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
            "active": False,
            "opponent": None,
            "days_left": 0,
            "weight_cut": None,
            "peak": False
        },
        "scheduled_fight": {
            "opponent": None,
            "days_until_fight": 0,
            "purse": 0,
            "accepted": False,
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
        "xp_gain": updated_player["xp"],
        "fatigue_gain": updated_player["fatigue"],
        "current_xp": updated_player["xp"],
        "current_level": updated_player["level"],
        "updated_stat": updated_player["stats"][skill]
    }


@router.post("/start-camp/{player_name}/{opponent}/{days}")
def start_camp(player_name: str, opponent: str, days: int):
    if player_name not in players:
        return {"error": "Player not found"}

    players[player_name]["fight_camp"] = {
        "active": True,
        "opponent": opponent,
        "days_left": days,
        "weight_cut": "medium",
        "peak": False
    }

    return {
        "message": f"{player_name} started fight camp",
        "fight_camp": players[player_name]["fight_camp"]
    }


@router.post("/book-fight/{player_name}/{opponent}/{days}/{purse}")
def book_fight(player_name: str, opponent: str, days: int, purse: int):
    if player_name not in players:
        return {"error": "Player not found"}

    players[player_name]["scheduled_fight"] = {
        "opponent": opponent,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    return {
        "message": f"{player_name} booked to fight {opponent}",
        "scheduled_fight": players[player_name]["scheduled_fight"]
    }


@router.post("/simulate-fight/{player_name}")
def simulate_fight(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    player = players[player_name]

    player["scheduled_fight"]["completed"] = True
    player["fight_camp"]["active"] = False
    player["fatigue"] += 20

    return {
        "message": f"{player_name} completed fight",
        "fighter": player
    }


@router.get("/fighter-stats/{player_name}")
def fighter_stats(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    return players[player_name]
