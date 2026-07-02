import random

# Global relationship storage
relationships = {}


def ensure_handle(entity):
    """
    Ensures every entity has a unique handle.
    """
    if "handle" not in entity:
        entity["handle"] = entity["name"].lower().replace(" ", "_")
    return entity["handle"]


def initialize_relationship(entity):
    """
    Creates relationship buckets for an entity.
    """
    entity_id = ensure_handle(entity)

    if entity_id not in relationships:
        relationships[entity_id] = {
            "friends": [],
            "rivals": [],
            "dating": [],
            "supporters": []
        }

    return relationships[entity_id]


# Legacy compatibility for old imports
def init_relationship(entity):
    return initialize_relationship(entity)


def generate_random_relationship(entity, all_entities):
    """
    Randomly builds a relationship with another entity.
    """
    initialize_relationship(entity)

    entity_id = ensure_handle(entity)

    valid_targets = [
        target for target in all_entities
        if ensure_handle(target) != entity_id
    ]

    if not valid_targets:
        return None

    target = random.choice(valid_targets)
    target_id = ensure_handle(target)

    relationship_type = random.choice([
        "friends",
        "rivals",
        "dating",
        "supporters"
    ])

    if target_id not in relationships[entity_id][relationship_type]:
        relationships[entity_id][relationship_type].append(target_id)

    return {
        "type": relationship_type,
        "target": target["name"],
        "target_handle": target_id
    }


def generate_relationship_post(entity, all_entities):
    """
    Generates social posts based on relationships.
    """
    chance = random.randint(1, 100)

    if chance > 20:
        return None

    relation = generate_random_relationship(entity, all_entities)

    if not relation:
        return None

    if relation["type"] == "friends":
        return f"Shoutout to {relation['target']}."

    if relation["type"] == "rivals":
        return f"{relation['target']} can't mess with me."

    if relation["type"] == "dating":
        return f"Me and {relation['target']} locked in."

    if relation["type"] == "supporters":
        return f"Big love to {relation['target']} for the support."

    return None


def should_attack(entity, target):
    """
    Determines if entity should attack/rival target.
    """
    initialize_relationship(entity)

    entity_id = ensure_handle(entity)
    target_id = ensure_handle(target)

    return target_id in relationships[entity_id]["rivals"]


def should_support(entity, target):
    """
    Determines if entity supports target.
    """
    initialize_relationship(entity)

    entity_id = ensure_handle(entity)
    target_id = ensure_handle(target)

    return (
        target_id in relationships[entity_id]["friends"]
        or target_id in relationships[entity_id]["supporters"]
    )


def get_relationships(entity):
    """
    Returns all relationships for an entity.
    """
    entity_id = ensure_handle(entity)
    initialize_relationship(entity)

    return relationships[entity_id]
