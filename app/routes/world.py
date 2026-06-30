from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()

world_state = {
    "current_date": datetime(2026, 1, 1),
    "economy": "Stable",
    "fight_week": 1,
    "major_event": None
}

players = {
    "Devon Duffee": {
        "age": 19,
        "injured": False,
        "injury_days_left": 0,
        "fatigue": 20
    }
}


def process_daily_updates():
    for player in players.values():
        if player["injured"] and player["injury_days_left"] > 0:
            player["injury_days_left"] -= 1

            if player["injury_days_left"] == 0:
                player["injured"] = False

        if player["fatigue"] > 0:
            player["fatigue"] -= 1


@router.get("/world-state")
def get_world_state():
    return world_state


@router.get("/players-status")
def get_players_status():
    return players


@router.post("/advance-day")
def advance_day():
    world_state["current_date"] += timedelta(days=1)

    process_daily_updates()

    return {
        "message": "Day advanced",
        "new_date": world_state["current_date"]
    }


@router.post("/advance-week")
def advance_week():
    world_state["current_date"] += timedelta(days=7)
    world_state["fight_week"] += 1

    for _ in range(7):
        process_daily_updates()

    return {
        "message": "Week advanced",
        "new_date": world_state["current_date"]
    }


@router.post("/advance-month")
def advance_month():
    world_state["current_date"] += timedelta(days=30)

    for player in players.values():
        if world_state["current_date"].month == 1:
            player["age"] += 1

    for _ in range(30):
        process_daily_updates()

    return {
        "message": "Month advanced",
        "new_date": world_state["current_date"]
    }
