import random

relationship_data = {}


# ==========================
# INIT RELATIONSHIP NETWORK
# ==========================

def init_relationship(entity):
    handle = entity["handle"]

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
    init_relationship(entity_one)
    init_relationship(entity_two)

    handle_one = entity_one["handle"]
    handle_two = entity_two["handle"]

    if relation_type == "friend":
        if handle_two not in relationship_data[handle_one]["friends"]:
            relationship_data[handle_one]["friends"].append(handle_two)

    elif relation_type == "rival":
        if handle_two not in relationship_data[handle_one]["rivals"]:
            relationship_data[handle_one]["rivals"].append(handle_two)

    elif relation_type == "family":
        if handle_two not in relationship_data[handle_one]["family"]:
            relationship_data[handle_one]["family"].append(handle_two)

    elif relation_type == "romantic":
        if handle_two not in relationship_data[handle_one]["romantic"]:
            relationship_data[handle_one]["romantic"].append(handle_two)

    elif relation_type == "business":
        if handle_two not in relationship_data[handle_one]["business"]:
            relationship_data[handle_one]["business"].append(handle_two)

    elif relation_type == "mentor":
        if handle_two not in relationship_data[handle_one]["mentors"]:
            relationship_data[handle_one]["mentors"].append(handle_two)

    elif relation_type == "fan":
        if handle_two not in relationship_data[handle_one]["fans"]:
            relationship_data[handle_one]["fans"].append(handle_two)

    elif relation_type == "hater":
        if handle_two not in relationship_data[handle_one]["haters"]:
            relationship_data[handle_one]["haters"].append(handle_two)

    elif relation_type == "obsessed":
        if handle_two not in relationship_data[handle_one]["obsessed_by"]:
            relationship_data[handle_one]["obsessed_by"].append(handle_two)

    elif relation_type == "respect":
        if handle_two not in relationship_data[handle_one]["respected_by"]:
            relationship_data[handle_one]["respected_by"].append(handle_two)


# ==========================
# GET RELATIONSHIPS
# ==========================

def get_relationships(entity):
    init_relationship(entity)
    return relationship_data[entity["handle"]]


# ==========================
# RANDOM RELATIONSHIP BUILDER
# ==========================

def generate_random_relationship(entity, all_entities):
    init_relationship(entity)

    possible_targets = [
        x for x in all_entities
        if x["handle"] != entity["handle"]
    ]

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

    if target_handle in relationships["friends"]:
        return True

    if target_handle in relationships["family"]:
        return True

    if target_handle in relationships["romantic"]:
        return True

    return False


def should_attack(entity, target_handle):
    relationships = get_relationships(entity)

    if target_handle in relationships["rivals"]:
        return True

    if target_handle in relationships["haters"]:
        return True

    return False


def should_support(entity, target_handle):
    relationships = get_relationships(entity)

    if target_handle in relationships["fans"]:
        return True

    if target_handle in relationships["respected_by"]:
        return True

    return False
