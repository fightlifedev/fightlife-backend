from fastapi import APIRouter
from app.database import players_collection
from app.systems.training import train_player
import random

router = APIRouter()

players = {
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
            "days_until_fight": 4,
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

offers = {}

def simulate_fight(player, opponent):
    player_score = sum(player["stats"].values()) + random.randint(1, 20)
    opponent_score = sum(opponent["stats"].values()) + random.randint(1, 20)

    winner = player["name"] if player_score >= opponent_score else opponent["name"]
    method = random.choice(["Decision", "Submission", "TKO", "KO"])
    round_ended = random.randint(1, 5)
    damage = random.randint(10, 50)

    xp_rewards = {
        "Decision": 15,
        "Submission": 20,
        "TKO": 22,
        "KO": 25
    }

    winner_player = player if winner == player["name"] else opponent
    loser_player = opponent if winner == player["name"] else player

    winner_player["xp"] += xp_rewards[method]
    loser_player["xp"] += 5

    if winner_player["xp"] >= 50:
        winner_player["level"] += 1
        winner_player["xp"] -= 50

    if loser_player["xp"] >= 50:
        loser_player["level"] += 1
        loser_player["xp"] -= 50

    winner_player["record"]["wins"] += 1
    loser_player["record"]["losses"] += 1

    return {
        "winner": winner,
        "method": method,
        "round": round_ended,
        "damage": damage,
        "player_score": player_score,
        "opponent_score": opponent_score
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
    return players


@router.post("/train/{player_name}/{skill}")
def train(player_name: str, skill: str):
    if player_name not in players:
        return {"error": "Player not found"}

    player = players[player_name]

    if skill not in player["stats"]:
        return {"error": "Skill not found"}

    updated_player = train_player(player, skill)
    players[player_name] = updated_player

    return updated_player


@router.post("/start-camp/{player_name}/{opponent}/{days}")
def start_camp(player_name: str, opponent: str, days: int):
    if player_name not in players:
        return {"error": "Player not found"}

    if opponent not in players:
        return {"error": "Opponent not found"}

    players[player_name]["fight_camp"] = {
        "active": True,
        "opponent": opponent,
        "days_left": days,
        "weight_cut": "medium",
        "peak": False
    }

    players[opponent]["fight_camp"] = {
        "active": True,
        "opponent": player_name,
        "days_left": days,
        "weight_cut": "medium",
        "peak": False
    }

    return {
        "fighter": players[player_name],
        "opponent": players[opponent]
    }


@router.post("/book-fight/{player_name}/{opponent}/{days}/{purse}")
def book_fight(player_name: str, opponent: str, days: int, purse: int):
    if player_name not in players:
        return {"error": "Player not found"}

    if opponent not in players:
        return {"error": "Opponent not found"}

    players[player_name]["scheduled_fight"] = {
        "opponent": opponent,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    players[opponent]["scheduled_fight"] = {
        "opponent": player_name,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    players[player_name]["fight_camp"]["active"] = True
    players[player_name]["fight_camp"]["days_left"] = days
    players[player_name]["fight_camp"]["opponent"] = opponent

    players[opponent]["fight_camp"]["active"] = True
    players[opponent]["fight_camp"]["days_left"] = days
    players[opponent]["fight_camp"]["opponent"] = player_name

    return {
        "message": "Fight booked successfully",
        "fighter": players[player_name],
        "opponent": players[opponent]
    }


@router.post("/simulate-fight/{player_name}")
def run_fight(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    player = players[player_name]

    if not player["scheduled_fight"]["opponent"]:
        return {"error": "No fight scheduled"}

    opponent_name = player["scheduled_fight"]["opponent"]

    if opponent_name not in players:
        return {"error": "Opponent not found"}

    opponent = players[opponent_name]

    result = simulate_fight(player, opponent)

    # reset player
    player["fight_camp"] = {
        "active": False,
        "opponent": None,
        "days_left": 0,
        "weight_cut": None,
        "peak": False
    }

    player["scheduled_fight"] = {
        "opponent": None,
        "days_until_fight": 0,
        "purse": 0,
        "accepted": False,
        "completed": True
    }

    # reset opponent
    opponent["fight_camp"] = {
        "active": False,
        "opponent": None,
        "days_left": 0,
        "weight_cut": None,
        "peak": False
    }

    opponent["scheduled_fight"] = {
        "opponent": None,
        "days_until_fight": 0,
        "purse": 0,
        "accepted": False,
        "completed": True
    }

    return {
        "message": f"{player_name} completed fight",
        "result": result,
        "fighter": player,
        "opponent": opponent
    }

@router.post("/advance-day")
def advance_day():
    for fighter in players.values():

        # Fight camp countdown
        if fighter["fight_camp"]["active"]:
            fighter["fight_camp"]["days_left"] -= 1

            if fighter["fight_camp"]["days_left"] <= 7:
                fighter["fight_camp"]["peak"] = True

        # Scheduled fight countdown
        if fighter["scheduled_fight"]["accepted"]:
            fighter["scheduled_fight"]["days_until_fight"] -= 1

            # Training during camp
            fighter["stats"]["boxing"] += 1
            fighter["stats"]["wrestling"] += 1
            fighter["stats"]["cardio"] += 1
            fighter["fatigue"] += 5

            # Fight day reached
            if fighter["scheduled_fight"]["days_until_fight"] <= 0:
                run_fight(fighter["name"])

        # Injury recovery
        if fighter["injured"]:
            fighter["injury_days_left"] -= 1

            if fighter["injury_days_left"] <= 0:
                fighter["injured"] = False
                fighter["injury_days_left"] = 0

    return {
        "message": "1 day advanced",
        "players": players
    }

@router.post("/advance-week")
def advance_week():
    for _ in range(7):
        advance_day()

    return {
        "message": "7 days advanced",
        "players": players
    }


@router.get("/fighter-stats/{player_name}")
def fighter_stats(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    return players[player_name]
    
@router.post("/offer-contract/{player_name}")
def offer_contract(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    fighter = players[player_name]

    # Offer only if fighter has no fights yet
    if fighter["record"]["wins"] == 0 and fighter["record"]["losses"] == 0:
        contract_value = random.randint(20000, 100000)

        offers[player_name] = {
            "organization": "UFC",
            "value": contract_value,
            "accepted": False
        }

        return {
            "message": f"{player_name} received a contract offer",
            "offer": offers[player_name]
        }

    return {"message": "No contract offers available"}
    
@router.post("/accept-contract/{player_name}")
def accept_contract(player_name: str):
    if player_name not in offers:
        return {"error": "No contract offer found"}

    offers[player_name]["accepted"] = True

    players[player_name]["organization"] = offers[player_name]["organization"]
    players[player_name]["money"] += offers[player_name]["value"]

    return {
        "message": f"{player_name} signed with {offers[player_name]['organization']}",
        "fighter": players[player_name]
    }
