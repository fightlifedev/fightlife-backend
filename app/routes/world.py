from fastapi import APIRouter
from datetime import datetime, timedelta
from systems.injuries import injury_check

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
        "fatigue": 20
    }
}


@router.get("/world-state")
def get_world_state():
    return world_state


@router.post("/advance-day")
def advance_day():
    world_state["current_date"] += timedelta(days=1)

    for name, player in players.items():
        player["fatigue"] = max(0, player["fatigue"] - 1)

        if not player["injured"]:
            player = injury_check(player)
        else:
            player["injury_days_left"] -= 1

            if player["injury_days_left"] <= 0:
                player["injured"] = False

    return {
        "message": "Day advanced",
        "new_date": world_state["current_date"]
    }


@router.post("/advance-week")
def advance_week():
    for _ in range(7):
        advance_day()

    world_state["fight_week"] += 1

    return {
        "message": "Week advanced",
        "fight_week": world_state["fight_week"]
    }


@router.post("/advance-month")
def advance_month():
    for _ in range(30):
        advance_day()

    return {
        "message": "Month advanced",
        "current_date": world_state["current_date"]
    }


@router.get("/players-status")
def player_status():
    return players
