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


cagewire_feed = []


# ==========================
# POST TEMPLATES
# ==========================

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


# ==========================
# HANDLE SYSTEM
# ==========================

def generate_handle(entity):
    if "handle" in entity and entity["handle"]:
        return entity["handle"]

    name = entity.get("name", "unknown")
    clean = name.lower().replace(" ", "")

    options = [
        f"@{clean}",
        f"@real{clean}",
        f"@{clean}{random.randint(1,999)}"
    ]

    entity["handle"] = random.choice(options)

    return entity["handle"]


# ==========================
# DYNAMIC TIME
# ==========================

def generate_dynamic_timestamp():
    minutes_ago = random.randint(1, 1440)
    return str(datetime.now() - timedelta(minutes=minutes_ago))


# ==========================
# SHOULD POST
# ==========================

def should_post(entity):
    buzz_info = get_buzz(entity)

    base_chance = 5
    buzz_bonus = buzz_info.get("buzz", 0) // 5
    momentum_bonus = max(0, buzz_info.get("momentum", 0))

    final_chance = min(90, base_chance + buzz_bonus + momentum_bonus)

    roll = random.randint(1, 100)

    return roll <= final_chance


# ==========================
# ENGAGEMENT ENGINE
# ==========================

def generate_engagement(entity):
    social = get_social(entity)
    buzz_info = get_buzz(entity)

    followers = social["followers"]
    buzz = buzz_info["buzz"]

    base_reach = max(10, followers * 0.01)
    buzz_multiplier = 1 + (buzz / 100)

    likes = int(base_reach * buzz_multiplier * random.uniform(0.5, 2.5))

    comments = random.randint(
        max(1, likes // 20),
        max(2, likes // 5)
    )

    shares = random.randint(
        max(1, comments // 5),
        max(2, comments // 2)
    )

    return likes, comments, shares


# ==========================
# CREATE POST
# ==========================

def create_post(entity):
    if entity["type"] == "fighter":
        content = random.choice(fighter_posts)

    elif entity["type"] == "fan":
        content = random.choice(fan_posts)

    else:
        content = random.choice(general_posts)

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


# ==========================
# MAIN CYCLE
# ==========================

def run_cagewire_cycle():
    generated_posts = []

    # random world event may happen
    generate_world_event(world_entities)

    for entity in world_entities:
        generate_handle(entity)

        init_entity(entity)
        init_social(entity)
        update_buzz(entity)

        if should_post(entity):
            generated_posts.append(
                create_post(entity)
            )

    return generated_posts


# ==========================
# FEED
# ==========================

def get_feed():
    return sorted(
        cagewire_feed,
        key=lambda x: x["timestamp"],
        reverse=True
    )


# ==========================
# TRENDING
# ==========================

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
