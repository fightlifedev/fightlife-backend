import random

relationship_data = {}


# ==========================
# SAFE HANDLE GENERATOR
# ==========================

def ensure_handle(entity):
    if "handle" not in entity:
        entity["handle"] = "@" + entity["name"].lower().replace(" ", ".")

    return entity["handle"]


# ==========================
# INIT RELATIONSHIP NETWORK
# ==========================

def init_relationship(entity):
    handle = ensure_handle(entity)

    if handle not in relationship_data:
        relationship_data[handle] = {
            "friends": [],
            "rivals": [],
            "family": [],
            "romantic": [],
            "business": [],
            "mentors": [],
            "fans": [],
            "haters": [],
            "obsessed_by": [],
            "respected_by": []
        }


# ==========================
# ADD RELATIONSHIP
# ==========================

def add_relationship(entity_one, entity_two, relation_type):
    handle_one = ensure_handle(entity_one)
    handle_two = ensure_handle(entity_two)

    init_relationship(entity_one)
    init_relationship(entity_two)

    relation_map = {
        "friend": "friends",
        "rival": "rivals",
        "family": "family",
        "romantic": "romantic",
        "business": "business",
        "mentor": "mentors",
        "fan": "fans",
        "hater": "haters",
        "obsessed": "obsessed_by",
        "respect": "respected_by"
    }

    if relation_type in relation_map:
        bucket = relation_map[relation_type]

        if handle_two not in relationship_data[handle_one][bucket]:
            relationship_data[handle_one][bucket].append(handle_two)


# ==========================
# GET RELATIONSHIPS
# ==========================

def get_relationships(entity):
    handle = ensure_handle(entity)
    init_relationship(entity)
    return relationship_data[handle]


# ==========================
# RANDOM RELATIONSHIP BUILDER
# ==========================

def generate_random_relationship(entity, all_entities):
    ensure_handle(entity)
    init_relationship(entity)

    possible_targets = []

    for x in all_entities:
        ensure_handle(x)

        if x["handle"] != entity["handle"]:
            possible_targets.append(x)

    if not possible_targets:
        return None

    target = random.choice(possible_targets)

    relation_types = [
        "friend",
        "rival",
        "respect",
        "fan",
        "hater",
        "business"
    ]

    relation = random.choice(relation_types)

    add_relationship(entity, target, relation)

    return {
        "source": entity["handle"],
        "target": target["handle"],
        "type": relation
    }


# ==========================
# REACTION LOGIC
# ==========================

def should_defend(entity, target_handle):
    relationships = get_relationships(entity)

    return (
        target_handle in relationships["friends"]
        or target_handle in relationships["family"]
        or target_handle in relationships["romantic"]
    )


def should_attack(entity, target_handle):
    relationships = get_relationships(entity)

    return (
        target_handle in relationships["rivals"]
        or target_handle in relationships["haters"]
    )


def should_support(entity, target_handle):
    relationships = get_relationships(entity)

    return (
        target_handle in relationships["fans"]
        or target_handle in relationships["respected_by"]
    )
