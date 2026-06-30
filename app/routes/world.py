from fastapi import APIRouter
from datetime import datetime, timedelta
from app.systems.recovery import recover_player
from app.systems.fightcamp import advance_fight_camp
from app.routes.players import players

router = APIRouter()

world_state = {
    "current_date": datetime(2026, 1, 1),
    "economy": "stable",
    "fight_week": 1,
    "major_event": None
}


@router.get("/world-state")
def get_world_state():
    return world_state


@router.post("/advance-day")
def advance_day():
    world_state["current_date"] += timedelta(days=1)

    for player_name in players:
        players[player_name] = recover_player(players[player_name])
        players[player_name] = advance_fight_camp(players[player_name])

    return {
        "message": "Day advanced",
        "new_date": world_state["current_date"],
        "players": players
    }


@router.get("/players-status")
def player_status():
    return players
