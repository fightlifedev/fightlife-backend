from fastapi import APIRouter
import random

router = APIRouter()


# =========================
# PLAYER DATABASE (V2)
# =========================

players = {
    "Devon Duffee": {
        "is_user": True,

        "identity": {
            "full_name": "Devon Elias Duffee",
            "nickname": "The Construct",
            "age": 19,
            "hometown": "Detroit",
            "nationality": "USA"
        },

        "life": {
            "career_path": "Combat Sports",
            "status": "Amateur",
            "education": "High School Graduate",
            "relationships": [],
            "social_circle": []
        },

        "career": {
            "industry": "Combat Sports",
            "league": None,
            "contracted": False,
            "champion": False,

            "amateur_record": {
                "wins": 18,
                "losses": 1
            },

            "pro_record": {
                "wins": 0,
                "losses": 0
            },

            "accolades": [],
            "rank": None
        },

        "finances": {
            "cash": 0,
            "bank": 0,
            "debt": 0,
            "income_streams": [],
            "assets": []
        },

        "reputation": {
            "global": 18,
            "industry": 45,
            "local": 90,
            "hype": 80
        },

        "attributes": {
            "potential": 95,
            "morale": 100,
            "fatigue": 10,
            "discipline": 88,
            "confidence": 92
        },

        "skills": {
            "physical": {
                "speed": 90,
                "power": 88,
                "endurance": 87
            },

            "combat": {
                "boxing": 83,
                "wrestling": 80,
                "cardio": 77
            },

            "mental": {
                "fight_iq": 85,
                "adaptability": 82,
                "killer_instinct": 90
            },

            "social": {
                "charisma": 78,
                "media_skill": 81
            }
        },

        "progression": {
            "xp": 23,
            "level": 1
        },

        "health": {
            "injured": False,
            "injury_days_left": 0,
            "recovering": False,
            "recovery_days_left": 0
        },

        "personality": {
            "discipline": 88,
            "aggression": 75,
            "loyalty": 60,
            "greed": 45,
            "risk_tolerance": 80
        },

        "emotions": {
            "anger": 10,
            "fear": 5,
            "confidence": 90,
            "motivation": 95
        },

        "memory": [],

        "goals": [
            "Become UFC champion",
            "Become a millionaire",
            "Build legacy"
        ],

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
        }
    },

    "Malik Brunson": {
        "is_user": False,

        "identity": {
            "full_name": "Malik Brunson",
            "nickname": "Napalm",
            "age": 19,
            "hometown": "Detroit",
            "nationality": "USA"
        },

        "life": {
            "career_path": "Combat Sports",
            "status": "Amateur",
            "education": "High School Graduate",
            "relationships": [],
            "social_circle": []
        },

        "career": {
            "industry": "Combat Sports",
            "league": None,
            "contracted": False,
            "champion": False,

            "amateur_record": {
                "wins": 11,
                "losses": 5
            },

            "pro_record": {
                "wins": 0,
                "losses": 0
            },

            "accolades": [],
            "rank": None
        },

        "finances": {
            "cash": 0,
            "bank": 0,
            "debt": 0,
            "income_streams": [],
            "assets": []
        },

        "reputation": {
            "global": 5,
            "industry": 15,
            "local": 30,
            "hype": 20
        },

        "attributes": {
            "potential": 78,
            "morale": 100,
            "fatigue": 5,
            "discipline": 70,
            "confidence": 65
        },

        "skills": {
            "physical": {
                "speed": 72,
                "power": 75,
                "endurance": 70
            },

            "combat": {
                "boxing": 72,
                "wrestling": 76,
                "cardio": 70
            },

            "mental": {
                "fight_iq": 67,
                "adaptability": 64,
                "killer_instinct": 68
            },

            "social": {
                "charisma": 52,
                "media_skill": 40
            }
        },

        "progression": {
            "xp": 8,
            "level": 1
        },

        "health": {
            "injured": False,
            "injury_days_left": 0,
            "recovering": False,
            "recovery_days_left": 0
        },

        "personality": {
            "discipline": 70,
            "aggression": 82,
            "loyalty": 55,
            "greed": 60,
            "risk_tolerance": 65
        },

        "emotions": {
            "anger": 20,
            "fear": 15,
            "confidence": 65,
            "motivation": 80
        },

        "memory": [],

        "goals": [
            "Turn pro",
            "Get signed",
            "Prove himself"
        ],

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
        }
    }
}


# =========================
# UTILITIES
# =========================

def add_memory(player, event):
    player["memory"].append(event)


def level_check(player):
    while player["progression"]["xp"] >= player["progression"]["level"] * 100:
        player["progression"]["xp"] -= player["progression"]["level"] * 100
        player["progression"]["level"] += 1


# =========================
# FIGHT SYSTEM
# =========================

def simulate_fight(player, opponent):
    player_score = (
        sum(player["skills"]["combat"].values())
        + sum(player["skills"]["physical"].values())
        + random.randint(1, 20)
    )

    opponent_score = (
        sum(opponent["skills"]["combat"].values())
        + sum(opponent["skills"]["physical"].values())
        + random.randint(1, 20)
    )

    winner = player if player_score >= opponent_score else opponent
    loser = opponent if winner == player else player

    method = random.choice(["Decision", "Submission", "TKO", "KO"])
    round_ended = random.randint(1, 5)

    winner["career"]["pro_record"]["wins"] += 1
    loser["career"]["pro_record"]["losses"] += 1

    winner["progression"]["xp"] += 25
    loser["progression"]["xp"] += 10

    level_check(winner)
    level_check(loser)

    winner["attributes"]["fatigue"] += 15
    loser["attributes"]["fatigue"] += 20

    winner["health"]["recovering"] = True
    loser["health"]["recovering"] = True

    winner["health"]["recovery_days_left"] = random.randint(3, 7)
    loser["health"]["recovery_days_left"] = random.randint(5, 10)

    if random.randint(1, 100) <= 20:
        loser["health"]["injured"] = True
        loser["health"]["injury_days_left"] = random.randint(7, 30)

    add_memory(winner, f"Defeated {loser['identity']['full_name']} by {method}")
    add_memory(loser, f"Lost to {winner['identity']['full_name']} by {method}")

    return {
        "winner": winner["identity"]["full_name"],
        "loser": loser["identity"]["full_name"],
        "method": method,
        "round": round_ended
    }


# =========================
# ROUTES
# =========================

@router.post("/book-fight/{player_name}/{opponent_name}/{days}")
def book_fight(player_name: str, opponent_name: str, days: int):
    player = players[player_name]
    opponent = players[opponent_name]

    purse = random.randint(5000, 25000)

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
        "message": "Fight booked",
        "fighter": player,
        "opponent": opponent
    }


@router.post("/start-camp/{player_name}")
def start_camp(player_name: str):
    fighter = players[player_name]

    if fighter["scheduled_fight"]["opponent"]:
        fighter["fight_camp"]["active"] = True
        fighter["fight_camp"]["opponent"] = fighter["scheduled_fight"]["opponent"]
        fighter["fight_camp"]["days_left"] = fighter["scheduled_fight"]["days_until_fight"]

    return fighter


@router.post("/run-fight/{player_name}")
def run_fight(player_name: str):
    player = players[player_name]
    opponent = players[player["scheduled_fight"]["opponent"]]

    result = simulate_fight(player, opponent)

    player["fight_camp"]["active"] = False
    opponent["fight_camp"]["active"] = False

    player["scheduled_fight"]["completed"] = True
    opponent["scheduled_fight"]["completed"] = True

    return result


@router.post("/advance-day")
def advance_day():
    for player_name, fighter in players.items():

        # AI auto starts camp
        if (
            not fighter["is_user"]
            and fighter["scheduled_fight"]["opponent"]
            and not fighter["fight_camp"]["active"]
        ):
            if random.randint(1, 100) <= 15:
                fighter["fight_camp"]["active"] = True
                fighter["fight_camp"]["opponent"] = fighter["scheduled_fight"]["opponent"]
                fighter["fight_camp"]["days_left"] = fighter["scheduled_fight"]["days_until_fight"]

        # Camp progression
        if fighter["fight_camp"]["active"]:
            fighter["fight_camp"]["days_left"] -= 1
            fighter["attributes"]["fatigue"] += 5

            fighter["skills"]["combat"]["boxing"] += 1
            fighter["skills"]["combat"]["wrestling"] += 1
            fighter["skills"]["combat"]["cardio"] += 1

            if fighter["fight_camp"]["days_left"] <= 7:
                fighter["fight_camp"]["peak"] = True

        # Fight countdown
        if fighter["scheduled_fight"]["accepted"]:
            fighter["scheduled_fight"]["days_until_fight"] -= 1

        # Auto fight
        if (
            fighter["scheduled_fight"]["days_until_fight"] <= 0
            and fighter["scheduled_fight"]["opponent"]
        ):
            run_fight(player_name)

        # Recovery
        if fighter["health"]["recovering"]:
            fighter["health"]["recovery_days_left"] -= 1

            if fighter["health"]["recovery_days_left"] <= 0:
                fighter["health"]["recovering"] = False

        # Injury healing
        if fighter["health"]["injured"]:
            fighter["health"]["injury_days_left"] -= 1

            if fighter["health"]["injury_days_left"] <= 0:
                fighter["health"]["injured"] = False

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
    return players[player_name]
