import random

buzz_data = {}


# ==========================
# SAFE HANDLE GENERATOR
# ==========================

def ensure_handle(entity):
    if "handle" not in entity:
        entity["handle"] = "@" + entity["name"].lower().replace(" ", ".")

    return entity["handle"]


# ==========================
# INIT ENTITY BUZZ
# ==========================

def init_entity(entity):
    entity_id = ensure_handle(entity)

    if entity_id not in buzz_data:
        buzz_data[entity_id] = {
            "buzz": random.randint(5, 40),
            "recent_event": None,
            "viral": False,
            "dead": False
        }


# ==========================
# GET BUZZ
# ==========================

def get_buzz(entity):
    entity_id = ensure_handle(entity)
    init_entity(entity)
    return buzz_data[entity_id]


# ==========================
# APPLY WORLD EVENT
# ==========================

def apply_event(entity, event_type):
    entity_id = ensure_handle(entity)
    init_entity(entity)

    if event_type == "death":
        buzz_data[entity_id]["buzz"] += random.randint(60, 200)
        buzz_data[entity_id]["recent_event"] = "death"

    elif event_type == "viral":
        buzz_data[entity_id]["buzz"] += random.randint(40, 120)
        buzz_data[entity_id]["recent_event"] = "viral"
        buzz_data[entity_id]["viral"] = True

    elif event_type == "scandal":
        buzz_data[entity_id]["buzz"] += random.randint(20, 80)
        buzz_data[entity_id]["recent_event"] = "scandal"

    elif event_type == "fight_win":
        buzz_data[entity_id]["buzz"] += random.randint(15, 60)
        buzz_data[entity_id]["recent_event"] = "fight_win"


# ==========================
# NATURAL BUZZ SHIFT
# ==========================

def update_buzz(entity):
    entity_id = ensure_handle(entity)
    init_entity(entity)

    change = random.randint(-8, 12)

    buzz_data[entity_id]["buzz"] += change

    if buzz_data[entity_id]["buzz"] < 0:
        buzz_data[entity_id]["buzz"] = 0


# ==========================
# TRENDING SYSTEM
# ==========================

def get_trending_entities(all_entities):
    valid_entities = []

    for entity in all_entities:
        ensure_handle(entity)
        init_entity(entity)

        valid_entities.append(entity)

    sorted_entities = sorted(
        valid_entities,
        key=lambda x: buzz_data[x["handle"]]["buzz"],
        reverse=True
    )

    return sorted_entities[:10]
