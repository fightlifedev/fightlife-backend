from fastapi import APIRouter
import random

router = APIRouter()

players = {
    "Devon Duffee": {
        "is_user": True,
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
        "recovering": False,
        "recovery_days_left": 0,

        "record": {
            "wins": 0,
            "losses": 0
        },

        "reputation": 12,
        "organization": "Independent",
        "money": 0
    },

    "Malik Brunson": {
        "is_user": False,
        "name": "Malik Brunson",
        "age": 27,
        "career": "MMA Fighter",
        "division": "Middleweight",
        "archetype": "Wrestler",
        "xp": 40,
        "fatigue": 5,
        "level": 2,
        "potential": 82,
        "morale": 100,
        "hometown": "Las Vegas",

        "stats": {
            "boxing": 75,
            "wrestling": 88,
            "power": 79,
            "cardio": 84
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
        "recovering": False,
        "recovery_days_left": 0,

        "record": {
            "wins": 4,
            "losses": 1
        },

        "reputation": 58,
        "organization": "UFC",
        "money": 185000
    }
}


offers = {}


def level_check(player):
    while player["xp"] >= player["level"] * 100:
        player["xp"] -= player["level"] * 100
        player["level"] += 1


def simulate_fight(player, opponent):
    player_score = sum(player["stats"].values()) + random.randint(1, 20)
    opponent_score = sum(opponent["stats"].values()) + random.randint(1, 20)

    winner = player if player_score >= opponent_score else opponent
    loser = opponent if winner == player else player

    method = random.choice(["Decision", "Submission", "TKO", "KO"])
    round_ended = random.randint(1, 5)

    xp_rewards = {
        "Decision": 15,
        "Submission": 20,
        "TKO": 22,
        "KO": 25
    }

    winner["xp"] += xp_rewards[method]
    loser["xp"] += 5

    level_check(winner)
    level_check(loser)

    winner["record"]["wins"] += 1
    loser["record"]["losses"] += 1

    damage = random.randint(0, 50)

    if damage >= 35:
        loser["injured"] = True
        loser["injury_days_left"] = random.randint(7, 30)

    winner["fatigue"] += 15
    loser["fatigue"] += 20

    winner["recovering"] = True
    loser["recovering"] = True
    winner["recovery_days_left"] = random.randint(3, 7)
    loser["recovery_days_left"] = random.randint(5, 10)

    winner["fight_camp"] = {
        "active": False,
        "opponent": None,
        "days_left": 0,
        "weight_cut": None,
        "peak": False
    }

    loser["fight_camp"] = {
        "active": False,
        "opponent": None,
        "days_left": 0,
        "weight_cut": None,
        "peak": False
    }

    winner["scheduled_fight"]["completed"] = True
    loser["scheduled_fight"]["completed"] = True

    return {
        "winner": winner["name"],
        "loser": loser["name"],
        "method": method,
        "round": round_ended
    }


@router.post("/book-fight/{player_name}/{opponent_name}/{days}")
def book_fight(player_name: str, opponent_name: str, days: int):
    player = players[player_name]
    opponent = players[opponent_name]

    purse = random.randint(10000, 25000)

    player["scheduled_fight"] = {
        "opponent": opponent_name,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    opponent["scheduled_fight"] = {
        "opponent": player_name,
        "days_until_fight": days,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    return {
        "message": "Fight booked successfully",
        "fighter": player,
        "opponent": opponent
    }


@router.post("/start-camp/{player_name}")
def start_camp(player_name: str):
    fighter = players[player_name]

    if fighter["scheduled_fight"]["opponent"]:
        days_until_fight = fighter["scheduled_fight"]["days_until_fight"]

        fighter["fight_camp"] = {
            "active": True,
            "opponent": fighter["scheduled_fight"]["opponent"],
            "days_left": days_until_fight,
            "weight_cut": "medium",
            "peak": False
        }

    return fighter


@router.post("/run-fight/{player_name}")
def run_fight(player_name: str):
    player = players[player_name]
    opponent_name = player["scheduled_fight"]["opponent"]
    opponent = players[opponent_name]

    result = simulate_fight(player, opponent)

    return {
        "message": f"{player_name} completed fight",
        "result": result,
        "fighter": player,
        "opponent": opponent
    }


@router.post("/advance-day")
def advance_day():
    for player_name, fighter in players.items():

        # AI auto starts camp
        if (
            not fighter["is_user"]
            and fighter["scheduled_fight"]["opponent"]
            and not fighter["fight_camp"]["active"]
        ):
            if fighter["scheduled_fight"]["days_until_fight"] > 14:
                if random.randint(1, 100) <= 15:
                    fighter["fight_camp"]["active"] = True
                    fighter["fight_camp"]["days_left"] = fighter["scheduled_fight"]["days_until_fight"]
                    fighter["fight_camp"]["opponent"] = fighter["scheduled_fight"]["opponent"]

        # Fight camp progression
        if fighter["fight_camp"]["active"]:
            fighter["fight_camp"]["days_left"] -= 1

            fighter["stats"]["boxing"] += 1
            fighter["stats"]["wrestling"] += 1
            fighter["stats"]["cardio"] += 1
            fighter["fatigue"] += 5

            if fighter["fight_camp"]["days_left"] <= 7:
                fighter["fight_camp"]["peak"] = True

        # Fight countdown
        if fighter["scheduled_fight"]["accepted"]:
            fighter["scheduled_fight"]["days_until_fight"] -= 1

        # Auto fight trigger
        if fighter["scheduled_fight"]["days_until_fight"] <= 0:
            if fighter["scheduled_fight"]["opponent"]:
                run_fight(player_name)

        # Injury recovery
        if fighter["injured"]:
            fighter["injury_days_left"] -= 1

            if fighter["injury_days_left"] <= 0:
                fighter["injured"] = False
                fighter["injury_days_left"] = 0

        # General recovery
        if fighter["recovering"]:
            fighter["recovery_days_left"] -= 1

            if fighter["recovery_days_left"] <= 0:
                fighter["recovering"] = False
                fighter["recovery_days_left"] = 0

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
