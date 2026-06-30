from fastapi import APIRouter
from app.database import players_collection
from app.systems.training import train_player

router = APIRouter()

players = {
    "Devon Duffee": {
        "xp": 23,
        "fatigue": 15,
        "level": 1,
        "stats": {
            "boxing": 83,
            "wrestling": 80,
            "power": 88,
            "cardio": 77
        },
        "fight_camp": {
            "active": True,
            "opponent": "Malik Brunson",
            "days_left": 34,
            "weight_cut": "medium",
            "peak": False
        },
        "scheduled_fight": {
            "opponent": "Malik Brunson",
            "days_until_fight": 41,
            "purse": 15000,
            "accepted": True,
            "completed": False
        },
        "injured": False,
        "injury_days_left": 0
    }
}


@router.post("/players")
def create_player(player: dict):
    result = players_collection.insert_one(player)
    return {
        "message": "Player created",
        "player_id": str(result.inserted_id)
    }


@router.get("/players")
def get_players():
    players_list = list(players_collection.find({}, {"_id": 0}))
    return players_list


@router.post("/train/{player_name}/{skill}")
def train(player_name: str, skill: str):
    if player_name not in players:
        return {"error": "Player not found"}

    player = players[player_name]

    if skill not in player["stats"]:
        return {"error": "Skill not found"}

    updated_player = train_player(player, skill)
    players[player_name] = updated_player

    return {
        "message": f"{player_name} trained {skill}",
        "xp_gain": updated_player["xp"] - 0,
        "fatigue_gain": updated_player["fatigue"] - 0,
        "current_xp": updated_player["xp"],
        "current_level": updated_player["level"],
        "updated_stat": updated_player["stats"][skill]
    }


@router.get("/fighter-stats/{player_name}")
def fighter_stats(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    return players[player_name]
