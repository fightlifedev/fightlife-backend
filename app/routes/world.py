from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()

world_state = {
    "current_date": datetime(2026, 1, 1),
    "economy": "Stable",
    "fight_week": 1,
    "major_event": None
}

@router.get("/world-state")
def get_world_state():
    return {
        "current_date": world_state["current_date"],
        "economy": world_state["economy"],
        "fight_week": world_state["fight_week"],
        "major_event": world_state["major_event"]
    }

@router.post("/advance-day")
def advance_day():
    world_state["current_date"] += timedelta(days=1)
    return {
        "message": "Day advanced",
        "new_date": world_state["current_date"]
    }

@router.post("/advance-week")
def advance_week():
    world_state["current_date"] += timedelta(days=7)
    world_state["fight_week"] += 1
    return {
        "message": "Week advanced",
        "new_date": world_state["current_date"],
        "fight_week": world_state["fight_week"]
    }

@router.post("/advance-month")
def advance_month():
    world_state["current_date"] += timedelta(days=30)
    return {
        "message": "Month advanced",
        "new_date": world_state["current_date"]
    }
