import random
from app.systems.buzz_engine import apply_event

event_pool = [
    "viral",
    "death",
    "scandal",
    "fight_win"
]


def generate_world_event(entities):
    trigger = random.randint(1, 100)

    if trigger > 25:
        return None

    entity = random.choice(entities)
    event_type = random.choice(event_pool)

    apply_event(entity, event_type)

    return {
        "entity": entity["handle"],
        "event": event_type
    }
