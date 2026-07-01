import random

buzz_data = {}


def init_entity(entity):
    entity_id = entity["handle"]

    if entity_id not in buzz_data:
        buzz_data[entity_id] = {
            "buzz": random.randint(5, 40),
            "momentum": random.randint(-5, 5),
            "controversy": random.randint(0, 30),
            "fan_loyalty": random.randint(20, 100),
            "viral": False,
            "dead": False,
            "recent_event": None
        }


def get_buzz(entity):
    return buzz_data.get(entity["handle"], {})


def apply_event(entity, event_type):
    init_entity(entity)

    if event_type == "viral":
        buzz_data[entity["handle"]]["buzz"] += random.randint(30, 80)
        buzz_data[entity["handle"]]["momentum"] += random.randint(10, 40)
        buzz_data[entity["handle"]]["viral"] = True

    elif event_type == "death":
        buzz_data[entity["handle"]]["buzz"] += random.randint(50, 200)
        buzz_data[entity["handle"]]["dead"] = True

    elif event_type == "scandal":
        buzz_data[entity["handle"]]["buzz"] += random.randint(20, 60)
        buzz_data[entity["handle"]]["controversy"] += random.randint(20, 50)

    elif event_type == "fight_win":
        buzz_data[entity["handle"]]["buzz"] += random.randint(15, 40)
        buzz_data[entity["handle"]]["momentum"] += random.randint(5, 15)

    buzz_data[entity["handle"]]["recent_event"] = event_type


def update_buzz(entity):
    init_entity(entity)

    data = buzz_data[entity["handle"]]

    change = random.randint(-5, 8)
    data["buzz"] += change + data["momentum"]

    if data["viral"]:
        data["buzz"] -= random.randint(5, 15)

    if data["dead"]:
        data["buzz"] += random.randint(-3, 10)

    data["buzz"] = max(0, data["buzz"])
    data["momentum"] = max(-50, min(50, data["momentum"]))


def get_trending_entities(entities):
    ranked = sorted(
        entities,
        key=lambda x: buzz_data.get(x["handle"], {}).get("buzz", 0),
        reverse=True
    )

    return ranked[:10]
