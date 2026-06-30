from fastapi import APIRouter
from app.systems.training import train_player
from app.systems.fight_engine import simulate_fight

router = APIRouter()

players = {
    "Devon Duffee": {
        "xp": 0,
        "level": 1,
        "potential": 50,
        "fatigue": 0,
        "injured": False,
        "injury_days_left": 0,
        "stats": {
            "boxing": 82,
            "wrestling": 80,
            "power": 88,
            "cardio": 77
        },
        "fight_camp": {
            "active": False,
            "opponent": None,
            "days_left": 0
        },
        "scheduled_fight": {
            "opponent": None,
            "days_until_fight": 0,
            "purse": 0,
            "accepted": False,
            "completed": False
        }
    },

    "Malik Brunson": {
        "xp": 0,
        "level": 1,
        "potential": 48,
        "fatigue": 0,
        "injured": False,
        "injury_days_left": 0,
        "stats": {
            "boxing": 78,
            "wrestling": 75,
            "power": 81,
            "cardio": 74
        },
        "fight_camp": {
            "active": False,
            "opponent": None,
            "days_left": 0
        },
        "scheduled_fight": {
            "opponent": None,
            "days_until_fight": 0,
            "purse": 0,
            "accepted": False,
            "completed": False
        }
    }
}


@router.post("/train/{player_name}/{skill}")
def train(player_name: str, skill: str):
    player = players[player_name]
    updated_player = train_player(player, skill)
    players[player_name] = updated_player
    return updated_player


@router.post("/simulate-fight/{player_name}")
def run_fight(player_name: str):
    player = players[player_name]

    opponent_name = player["scheduled_fight"]["opponent"]

    if not opponent_name:
        return {"error": "No scheduled opponent"}

    opponent = players[opponent_name]

    result = simulate_fight(player, opponent)

    player["scheduled_fight"]["completed"] = True

    return {
        "fight_result": result,
        "player": player_name,
        "opponent": opponent_name
    }


@router.get("/fighter-stats/{player_name}")
def fighter_stats(player_name: str):
    return players[player_name]
