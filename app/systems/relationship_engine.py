import random


relationships = {}


# ==========================
# SAFE HANDLE CREATOR
# ==========================

def ensure_handle(entity):
    if "handle" not in entity:
        entity["handle"] = "@" + entity["name"].lower().replace(" ", ".")

    return entity["handle"]


# ==========================
# INIT RELATIONSHIPS
# ==========================

def init_relationship(entity):
    entity_id = ensure_handle(entity)

    if entity_id not in relationships:
        relationships[entity_id] = {
            "friends": [],
            "rivals": [],
            "dating": [],
            "family": []
        }


# ==========================
# GET RELATIONSHIP DATA
# ==========================

def get_relationships(entity):
    entity_id = ensure_handle(entity)
    init_relationship(entity)
    return relationships[entity_id]


# ==========================
# CREATE RANDOM RELATIONSHIP
# ==========================

def generate_random_relationship(entity, all_entities):
    entity_id = ensure_handle(entity)
    init_relationship(entity)

    valid_targets = []

    for x in all_entities:
        ensure_handle(x)

        if x["handle"] != entity["handle"]:
            valid_targets.append(x)

    if not valid_targets:
        return None

    target = random.choice(valid_targets)

    relation_type = random.choice([
        "friends",
        "rivals",
        "dating"
    ])

    relationships[entity_id][relation_type].append(target["handle"])

    return {
        "type": relation_type,
        "target": target["name"]
    }


# ==========================
# GET RANDOM RELATIONSHIP POST
# ==========================

def generate_relationship_post(entity, all_entities):
    entity_id = ensure_handle(entity)
    init_relationship(entity)

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

    return None
# ==========================
# LEGACY COMPATIBILITY
# ==========================

def should_defend(entity, target):
    init_relationship(entity)
    entity_id = ensure_handle(entity)

    if target["handle"] in relationships[entity_id]["friends"]:
        return True

    return False
    
def should_attack(entity, target):
    init_relationship(entity)
    entity_id = ensure_handle(entity)

    ensure_handle(target)

    if target["handle"] in relationships[entity_id]["rivals"]:
        return True

    return False
