import random
from datetime import datetime, timedelta

from app.entities.world_entities import world_entities
from app.systems.buzz_engine import (
    init_entity,
    get_buzz,
    update_buzz,
    get_trending_entities
)
from app.systems.event_engine import generate_world_event
from app.systems.social_graph import init_social, get_social
from app.systems.personality_engine import (
    init_personality,
    get_posting_weight,
    should_start_drama,
    should_capitalize_event
)
from app.systems.relationship_engine import (
    init_relationship,
    generate_random_relationship,
    should_defend,
    should_attack,
    should_support
)

cagewire_feed = []

fighter_posts = [
    "Camp going crazy.",
    "Locked in.",
    "New fight news soon.",
    "Nobody can stop me.",
    "Focused.",
]

fan_posts = [
    "That fight was wild.",
    "He got robbed.",
    "Future champ.",
    "This division crazy."
]

general_posts = [
    "Big news soon.",
    "What a day.",
    "Life moving fast."
]

defense_posts = [
    "Y'all need to chill.",
    "Stop disrespecting him.",
    "He'll bounce back."
]

attack_posts = [
    "Told y'all he was overrated.",
    "Fraud.",
    "He ain't built for this."
]

support_posts = [
    "Still my favorite.",
    "Always rocking with you.",
    "Real ones know."
]

drama_posts = [
    "Stop mentioning my name.",
    "Keep talking.",
    "Say it to my face."
]


def generate_handle(entity):
    if "handle" in entity:
        return entity["handle"]

    entity["handle"] = "@" + entity["name"].lower().replace(" ", ".")
    return entity["handle"]


def generate_dynamic_timestamp():
    minutes_ago = random.randint(1, 1440)
    return str(datetime.now() - timedelta(minutes=minutes_ago))


def should_post(entity):
    buzz = get_buzz(entity)
    posting_weight = get_posting_weight(entity)

    final_score = posting_weight + buzz.get("buzz", 0)

    return random.randint(1, 200) <= final_score


def generate_engagement(entity):
    social = get_social(entity)
    buzz = get_buzz(entity)

    followers = social["followers"]
    buzz_score = buzz["buzz"]

    reach = followers * random.uniform(0.01, 0.06)

    if buzz_score > 80:
        reach *= random.uniform(2, 4)

    likes = int(reach)

    comments = random.randint(
        max(1, int(likes * 0.03)),
        max(2, int(likes * 0.15))
    )

    shares = random.randint(
        max(1, int(comments * 0.05)),
        max(2, int(comments * 0.30))
    )

    return likes, comments, shares


def generate_relationship_post(entity):
    target = random.choice(world_entities)

    if target["handle"] == entity["handle"]:
        return None

    if should_defend(entity, target["handle"]):
        return random.choice(defense_posts)

    if should_attack(entity, target["handle"]):
        return random.choice(attack_posts)

    if should_support(entity, target["handle"]):
        return random.choice(support_posts)

    return None


def generate_content(entity):
    relation_post = generate_relationship_post(entity)

    if relation_post:
        return relation_post

    if should_start_drama(entity):
        return random.choice(drama_posts)

    recent_event = get_buzz(entity).get("recent_event")

    if recent_event and should_capitalize_event(entity):
        if recent_event == "death":
            return "Rest easy."

        if recent_event == "viral":
            return "Appreciate the love."

        if recent_event == "scandal":
            return "Truth always wins."

        if recent_event == "fight_win":
            return "Told y'all."

    if entity["type"] == "fighter":
        return random.choice(fighter_posts)

    if entity["type"] == "fan":
        return random.choice(fan_posts)

    return random.choice(general_posts)


def create_post(entity):
    content = generate_content(entity)

    likes, comments, shares = generate_engagement(entity)

    post = {
        "author": entity["name"],
        "handle": entity["handle"],
        "verified": entity.get("verified", False),
        "content": content,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "timestamp": generate_dynamic_timestamp(),
        "buzz": get_buzz(entity)["buzz"],
        "recent_event": get_buzz(entity)["recent_event"]
    }

    cagewire_feed.append(post)

    return post


def run_cagewire_cycle():
    generated_posts = []

    generate_world_event(world_entities)

    for entity in world_entities:
        generate_handle(entity)

        init_entity(entity)
        init_social(entity)
        init_personality(entity)
        init_relationship(entity)

        if random.randint(1, 100) <= 15:
            generate_random_relationship(entity, world_entities)

        update_buzz(entity)

        if should_post(entity):
            generated_posts.append(
                create_post(entity)
            )

    return generated_posts


def get_feed():
    return sorted(
        cagewire_feed,
        key=lambda x: x["timestamp"],
        reverse=True
    )


def get_trending_posts():
    trending_entities = get_trending_entities(world_entities)

    trending_posts = []

    for entity in trending_entities:
        for post in cagewire_feed:
            if post["handle"] == entity["handle"]:
                trending_posts.append(post)

    return sorted(
        trending_posts,
        key=lambda x: x["buzz"],
        reverse=True
    )[:10]
