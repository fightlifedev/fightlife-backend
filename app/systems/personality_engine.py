import random


# personality storage
personality_data = {}


def init_personality(entity):
    entity_id = entity["handle"]

    if entity_id not in personality_data:
        personality_data[entity_id] = {
            "ego": random.randint(1, 100),
            "aggression": random.randint(1, 100),
            "discipline": random.randint(1, 100),
            "loyalty": random.randint(1, 100),
            "clout_chasing": random.randint(1, 100),
            "emotional_control": random.randint(1, 100),
            "confidence": random.randint(1, 100),
            "risk_taking": random.randint(1, 100),
            "posting_frequency": random.choice([
                "very_low",
                "low",
                "medium",
                "high",
                "very_high"
            ]),
            "drama_likelihood": random.randint(1, 100),
            "opportunism": random.randint(1, 100),
            "grief_tolerance": random.randint(1, 100)
        }


def get_personality(entity):
    return personality_data.get(entity["handle"], {})


def get_posting_weight(entity):
    traits = get_personality(entity)

    frequency_map = {
        "very_low": 5,
        "low": 15,
        "medium": 35,
        "high": 60,
        "very_high": 85
    }

    frequency = frequency_map.get(
        traits.get("posting_frequency", "medium"),
        35
    )

    clout_bonus = traits.get("clout_chasing", 0) // 5
    ego_bonus = traits.get("ego", 0) // 8
    confidence_bonus = traits.get("confidence", 0) // 10

    return frequency + clout_bonus + ego_bonus + confidence_bonus


def should_start_drama(entity):
    traits = get_personality(entity)

    score = (
        traits.get("aggression", 0) +
        traits.get("ego", 0) +
        traits.get("drama_likelihood", 0)
    )

    return random.randint(1, 300) <= score


def should_capitalize_event(entity):
    traits = get_personality(entity)

    score = (
        traits.get("clout_chasing", 0) +
        traits.get("opportunism", 0)
    )

    return random.randint(1, 200) <= score


def react_to_death(entity):
    traits = get_personality(entity)

    grief = traits.get("grief_tolerance", 50)
    loyalty = traits.get("loyalty", 50)

    if grief < 30:
        return "unfollow"

    if loyalty > 75:
        return "tribute"

    return "ignore"
