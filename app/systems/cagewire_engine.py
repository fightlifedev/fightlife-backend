import random

from app.entities.world_entities import world_entities
from app.systems.relationship_engine import (
    generate_relationship_post,
    should_attack,
    should_support,
    should_defend,
    ensure_handle
)


POST_TEMPLATES = {
    "fighter": [
        "Training hard. Stay ready.",
        "Big fight coming soon.",
        "Nobody can stop me.",
        "Legacy over everything."
    ],
    "artist": [
        "New music dropping soon.",
        "Studio all night.",
        "Album mode activated.",
        "Big collab on the way."
    ],
    "athlete": [
        "Locked in for the season.",
        "Work speaks louder than words.",
        "Another day. Another grind."
    ],
    "celebrity": [
        "Big moves behind the scenes.",
        "Life been wild lately.",
        "Blessed beyond measure."
    ],
    "business": [
        "Big expansion coming.",
        "New partnership announced.",
        "Business never sleeps."
    ],
    "media": [
        "Breaking story coming soon.",
        "Sources say something major is happening.",
        "Stay tuned."
    ]
}


def get_entity_type(entity):
    return entity.get("type", "celebrity")


def generate_base_post(entity):
    entity_type = get_entity_type(entity)

    if entity_type not in POST_TEMPLATES:
        entity_type = "celebrity"

    return random.choice(POST_TEMPLATES[entity_type])


def generate_attack_post(entity):
    possible_targets = [
        x for x in world_entities
        if ensure_handle(x) != ensure_handle(entity)
    ]

    if not possible_targets:
        return None

    target = random.choice(possible_targets)

    if should_attack(entity, target):
        return f"{target['name']} ain't on my level."

    return None


def generate_support_post(entity):
    possible_targets = [
        x for x in world_entities
        if ensure_handle(x) != ensure_handle(entity)
    ]

    if not possible_targets:
        return None

    target = random.choice(possible_targets)

    if should_support(entity, target):
        return f"Respect to {target['name']}."

    return None


def generate_defense_post(entity):
    possible_targets = [
        x for x in world_entities
        if ensure_handle(x) != ensure_handle(entity)
    ]

    if not possible_targets:
        return None

    target = random.choice(possible_targets)

    if should_defend(entity, target):
        return f"I stand with {target['name']}."

    return None


def generate_content(entity):
    roll = random.randint(1, 100)

    if roll <= 40:
        return generate_base_post(entity)

    if roll <= 60:
        relation_post = generate_relationship_post(entity, world_entities)
        if relation_post:
            return relation_post

    if roll <= 75:
        attack_post = generate_attack_post(entity)
        if attack_post:
            return attack_post

    if roll <= 90:
        support_post = generate_support_post(entity)
        if support_post:
            return support_post

    defense_post = generate_defense_post(entity)
    if defense_post:
        return defense_post

    return generate_base_post(entity)


def create_post(entity):
    return {
        "author": ensure_handle(entity),
        "name": entity["name"],
        "content": generate_content(entity)
    }


def run_cagewire_cycle():
    posts = []

    active_entities = random.sample(
        world_entities,
        min(10, len(world_entities))
    )

    for entity in active_entities:
        posts.append(create_post(entity))

    return posts
    
def get_feed():
    return run_cagewire_cycle()
