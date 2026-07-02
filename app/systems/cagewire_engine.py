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


cagewire_feed = []


fighter_posts = [
    "Camp going crazy.",
    "Locked in.",
    "New fight news soon.",
    "Nobody can stop me.",
    "Focused.",
    "Grinding every day.",
    "Respect to my opponent."
]

fan_posts = [
    "That fight was wild.",
    "He got robbed.",
    "Future champ.",
    "This division crazy.",
    "I called it."
]

general_posts = [
    "Big news soon.",
    "What a day.",
    "Life moving fast.",
    "Staying focused."
]

drama_posts = [
    "Stop mentioning my name.",
    "Say it to my face.",
    "You know what it is.",
    "I'm not ducking nobody.",
    "Keep talking."
]


def generate_handle(entity):
    if "handle" in entity and entity["handle"]:
        return entity["handle"]

    name = entity.get("name", "unknown")
    clean = name.lower().replace(" ", ".")

    entity["handle"] = f"@{clean}"
    return entity["handle"]


def generate_dynamic_timestamp():
    minutes_ago = random.randint(1, 1440)
    return str(datetime.now() - timedelta(minutes=minutes_ago))


def should_post(entity):
    buzz = get_buzz(entity)
    posting_weight = get_posting_weight(entity)

    buzz_bonus = buzz.get("buzz", 0) // 4
    momentum_bonus = max(0, buzz.get("momentum", 0))

    final_score = posting_weight + buzz_bonus + momentum_bonus

    return random.randint(1, 150) <= final_score


def generate_engagement(entity):
    social = get_social(entity)
    buzz = get_buzz(entity)

    followers = social["followers"]
    buzz_score = buzz["buzz"]

    reach = followers * random.uniform(0.01, 0.08)

    if buzz_score > 80:
        reach *= random.uniform(1.5, 4)

    likes = int(reach)

    comments = random.randint(
        max(1, int(likes * 0.03)),
        max(2, int(likes * 0.20))
    )

    shares = random.randint(
        max(1, int(comments * 0.10)),
        max(2, int(comments * 0.50))
    )

    return likes, comments, shares


def generate_content(entity):
    if should_start_drama(entity):
        return random.choice(drama_posts)

    recent_event = get_buzz(entity).get("recent_event")

    if recent_event and should_capitalize_event(entity):
        if recent_event == "death":
            return "Rest easy. Legends never die."

        if recent_event == "viral":
            return "Appreciate all the love."

        if recent_event == "scandal":
            return "Truth always comes out."

        if recent_event == "fight_win":
            return "Told y'all."

    if entity["type"] == "fighter":
        return random.choice(fighter_posts)

    elif entity["type"] == "fan":
        return random.choice(fan_posts)

    else:
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

    trending_posts = sorted(
        trending_posts,
        key=lambda x: x["buzz"],
        reverse=True
    )

    return trending_posts[:10]
