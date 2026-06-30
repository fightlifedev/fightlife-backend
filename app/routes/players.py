from fastapi import APIRouter
from app.database import players_collection
from app.systems.training import train_player

router = APIRouter()

players = {
    "Devon Duffee": {
        "xp": 0,
        "fatigue": 0,
        "stats": {
            "boxing": 82,
            "wrestling": 80,
            "power": 88,
            "cardio": 77
        }
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
        "xp": updated_player["xp"],
        "fatigue": updated_player["fatigue"],
        "updated_stat": updated_player["stats"][skill]
    }


@router.get("/fighter-stats/{player_name}")
def fighter_stats(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    return players[player_name]
