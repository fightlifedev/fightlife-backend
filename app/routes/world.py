from fastapi import APIRouter
from datetime import datetime, timedelta

from app.systems.recovery import recover_player
from app.systems.life_events import trigger_life_event
from app.routes.players import players

router = APIRouter()

# ============================
# WORLD STATE
# ============================

world_state = {
    "current_date": datetime(2026, 1, 1),
    "economy": "stable",
    "fight_week": 1,
    "major_event": None,
    "world_news": []
}


# ============================
# ADVANCE DAY
# ============================

@router.post("/advance-day")
def advance_day():
    world_state["current_date"] += timedelta(days=1)

    daily_events = []

    for player_name in players:
        fighter = players[player_name]

        # Recovery system
        players[player_name] = recover_player(fighter)

        # Fight camp countdown
        if fighter["fight_camp"]["active"]:
            fighter["fight_camp"]["days_left"] -= 1

            if fighter["fight_camp"]["days_left"] <= 0:
                fighter["fight_camp"]["active"] = False
                fighter["memory"].append("Fight camp completed.")

        # Scheduled fight countdown
        if fighter["scheduled_fight"]["accepted"]:
            fighter["scheduled_fight"]["days_until_fight"] -= 1

            if fighter["scheduled_fight"]["days_until_fight"] <= 0:
                fighter["scheduled_fight"]["completed"] = True
                fighter["memory"].append("Fight day has arrived.")

        # Dynamic life event system
        event = trigger_life_event(player_name)

        if event:
            daily_events.append({
                "player": player_name,
                "event": event
            })

    # Random economy shifts
    economy_roll = world_state["current_date"].day % 10

    if economy_roll == 3:
        world_state["economy"] = "booming"

    elif economy_roll == 7:
        world_state["economy"] = "recession"

    else:
        world_state["economy"] = "stable"

    world_state["world_news"] = daily_events

    return {
        "message": "Day advanced",
        "current_date": world_state["current_date"],
        "economy": world_state["economy"],
        "events": daily_events,
        "players": players
    }


# ============================
# ADVANCE WEEK
# ============================

@router.post("/advance-week")
def advance_week():
    weekly_events = []

    for _ in range(7):
        result = advance_day()

        if result["events"]:
            weekly_events.extend(result["events"])

    world_state["fight_week"] += 1

    return {
        "message": "Week advanced",
        "current_date": world_state["current_date"],
        "fight_week": world_state["fight_week"],
        "economy": world_state["economy"],
        "weekly_events": weekly_events
    }


# ============================
# WORLD STATE
# ============================

@router.get("/world-state")
def get_world_state():
    return world_state
