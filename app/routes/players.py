from fastapi import APIRouter
from app.database import players_collection
from app.systems.training import train_player

router = APIRouter()

players = {
    import random

def simulate_fight(player, opponent):
    player_score = (
        player["stats"]["boxing"] +
        player["stats"]["wrestling"] +
        player["stats"]["power"] +
        player["stats"]["cardio"] +
        random.randint(1, 20)
    )

    opponent_score = (
        opponent["stats"]["boxing"] +
        opponent["stats"]["wrestling"] +
        opponent["stats"]["power"] +
        opponent["stats"]["cardio"] +
        random.randint(1, 20)
    )

    if player_score > opponent_score:
        winner = player["name"]
        player["record"]["wins"] += 1
        opponent["record"]["losses"] += 1
        player["money"] += player["scheduled_fight"]["purse"]
        player["reputation"] += 5
    else:
        winner = opponent["name"]
        opponent["record"]["wins"] += 1
        player["record"]["losses"] += 1
        opponent["money"] += player["scheduled_fight"]["purse"]
        opponent["reputation"] += 5

    player["scheduled_fight"]["completed"] = True
    player["fight_camp"]["active"] = False
    player["fight_camp"]["opponent"] = None
    player["fight_camp"]["days_left"] = 0

    return {
        "winner": winner,
        "player_score": player_score,
        "opponent_score": opponent_score
    }
    "Devon Duffee": {
        "name": "Devon Elias Duffee",
        "age": 19,
        "career": "MMA Fighter",
        "division": "Light Heavyweight",
        "archetype": "Pressure Boxer",
        "xp": 23,
        "fatigue": 10,
        "level": 1,
        "potential": 95,
        "morale": 100,
        "hometown": "Detroit",
        "stats": {
            "boxing": 83,
            "wrestling": 80,
            "power": 88,
            "cardio": 77
        },
        "fight_camp": {
            "active": True,
            "opponent": "Malik Brunson",
            "days_left": 4,
            "weight_cut": "medium",
            "peak": False
        },
        "scheduled_fight": {
            "opponent": "Malik Brunson",
            "days_until_fight": 9,
            "purse": 15000,
            "accepted": True,
            "completed": False
        },
        "injured": False,
        "injury_days_left": 0,
        "record": {
            "wins": 0,
            "losses": 0
        },
        "reputation": 20,
        "money": 10000
    },

    "Malik Brunson": {
        "name": "Malik Brunson",
        "age": 21,
        "career": "MMA Fighter",
        "division": "Light Heavyweight",
        "archetype": "Wrestler",
        "xp": 0,
        "fatigue": 0,
        "level": 1,
        "potential": 76,
        "morale": 88,
        "hometown": "Atlanta",
        "stats": {
            "boxing": 78,
            "wrestling": 76,
            "power": 82,
            "cardio": 80
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
        "injury_days_left": 0,
        "record": {
            "wins": 0,
            "losses": 0
        },
        "reputation": 12,
        "money": 5000
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
def run_fight(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    player = players[player_name]

    if "scheduled_fight" not in player:
        return {"error": "No fight scheduled"}

    opponent_name = player["scheduled_fight"]["opponent"]

    if opponent_name not in players:
        return {"error": "Opponent not found"}

    opponent = players[opponent_name]

    result = simulate_fight(player, opponent)

    return {
        "message": f"{player_name} completed fight",
        "result": result,
        "fighter": player
    }


@router.get("/fighter-stats/{player_name}")
def fighter_stats(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    return players[player_name]
