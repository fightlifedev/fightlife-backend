import random
from app.entities.world_entities import world_entities


# ============================
# CAGEWIRE POST TEMPLATES
# ============================

post_templates = {
    "fighter": [
        "Training hard. Stay ready.",
        "Big fight news coming soon.",
        "Nobody in my division can stop me.",
        "Respect to all warriors.",
        "New contract signed. Time to work."
    ],

    "media": [
        "BREAKING: Massive fight announced.",
        "Sources say a top contender is injured.",
        "Rumors are heating up in the MMA world.",
        "Major contract signed today.",
        "Fight world buzzing after today's events."
    ],

    "promotion": [
        "New fight card dropping soon.",
        "Tickets on sale now.",
        "Championship fight incoming.",
        "Fight week begins now.",
        "Big announcement tonight."
    ]
}


# ============================
# LIVE FEED
# ============================

cagewire_feed = []


# ============================
# GENERATE POSTS
# ============================

def generate_random_post():
    categories = ["fighters", "media", "promotions"]

    chosen_category = random.choice(categories)

    entity = random.choice(
        world_entities[chosen_category]
    )

    entity_type = entity["type"]

    if entity_type not in post_templates:
        return None

    content = random.choice(
        post_templates[entity_type]
    )

    post = {
        "author": entity["name"],
        "type": entity_type,
        "content": content,
        "likes": random.randint(1000, 500000),
        "comments": random.randint(50, 25000),
        "shares": random.randint(20, 10000)
    }

    cagewire_feed.append(post)

    return post


# ============================
# GET FEED
# ============================

def get_feed():
    return cagewire_feed[-25:]
