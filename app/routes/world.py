from fastapi import APIRouter
from datetime import datetime, timedelta
from app.systems.recovery import recover_player

router = APIRouter()

world_state = {
    "current_date": datetime(2026, 1, 1),
    "economy": "stable",
    "fight_week": 1,
    "major_event": None
}

players = {
    "Devon Duffee": {
        "age": 19,
        "injured": False,
        "injury_days_left": 0,
        "fatigue": 20,
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


@router.post("/advance-day")
def advance_day():
    world_state["current_date"] += timedelta(days=1)

    for player_name in players:
        players[player_name] = recover_player(players[player_name])

        if players[player_name]["fight_camp"]["active"]:
            players[player_name]["fight_camp"]["days_left"] -= 1

            if players[player_name]["fight_camp"]["days_left"] <= 0:
                players[player_name]["fight_camp"]["active"] = False

        if players[player_name]["scheduled_fight"]["accepted"]:
            players[player_name]["scheduled_fight"]["days_until_fight"] -= 1

            if players[player_name]["scheduled_fight"]["days_until_fight"] <= 0:
                players[player_name]["scheduled_fight"]["completed"] = True

    return {
        "message": "Day advanced",
        "current_date": world_state["current_date"],
        "players": players
    }


@router.get("/world-state")
def get_world_state():
    return world_state
