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
            "days_until_fight": 0,
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
         },
         }

def simulate_fight(player, opponent):
    ...
    player["scheduled_fight"]["completed"] = True
    player["fight_camp"]["active"] = False
    player["fight_camp"]["opponent"] = None
    player["fight_camp"]["days_left"] = 0

    # XP REWARDS
    xp_rewards = {
        "Split Decision": 12,
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

    # Schedule for player
    players[player_name]["scheduled_fight"] = {
        "opponent": opponent,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    # Schedule for opponent
    players[opponent]["scheduled_fight"] = {
        "opponent": player_name,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    # Put player in camp
    players[player_name]["fight_camp"] = {
        "active": True,
        "opponent": opponent,
        "days_left": days,
        "weight_cut": "medium",
        "peak": False
    }

    # Put opponent in camp
    players[opponent]["fight_camp"] = {
        "active": True,
        "opponent": player_name,
        "days_left": days,
        "weight_cut": "medium",
        "peak": False
    }

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

    # RESET PLAYER AFTER FIGHT
    player["fight_camp"]["active"] = False
    player["fight_camp"]["opponent"] = None
    player["fight_camp"]["days_left"] = 0
    player["fight_camp"]["peak"] = False

    player["scheduled_fight"] = {
        "opponent": None,
        "days_until_fight": 0,
        "purse": 0,
        "accepted": False,
        "completed": True
    }

    # RESET OPPONENT AFTER FIGHT
    opponent["fight_camp"]["active"] = False
    opponent["fight_camp"]["opponent"] = None
    opponent["fight_camp"]["days_left"] = 0
    opponent["fight_camp"]["peak"] = False

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

        # Fight camp progression
        if fighter["fight_camp"]["active"] == True:
            fighter["fight_camp"]["days_left"] -= 1

            if fighter["scheduled_fight"]["accepted"] == True:
                fighter["scheduled_fight"]["days_until_fight"] -= 1

            # Training gains
            fighter["stats"]["boxing"] += 1
            fighter["stats"]["wrestling"] += 1
            fighter["stats"]["cardio"] += 1

            # Fatigue rises
            fighter["fatigue"] += 5

            # Peak week trigger
            if fighter["fight_camp"]["days_left"] <= 7:
                fighter["fight_camp"]["peak"] = True

        # Injury recovery
        if fighter["injured"] == True:
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
