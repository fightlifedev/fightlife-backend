import random
from datetime import datetime
from app.entities.world_entities import world_entities


# =========================
# CAGEWIRE MASTER FEED
# =========================

cagewire_feed = []


# =========================
# POST TEMPLATES
# =========================

fighter_templates = [
    "Locked in. Camp starts now.",
    "Another body added to the list.",
    "I’m coming for gold.",
    "Nobody can stop me.",
    "Respect to my opponent. Big fight coming.",
    "Injury won’t stop me.",
    "Grinding while y’all sleep.",
    "Fight news dropping soon.",
    "Detroit made me.",
    "New contract. New chapter."
]

fan_templates = [
    "This dude is overrated.",
    "Future champ.",
    "That KO was insane.",
    "I got money on him.",
    "He’s ducking smoke.",
    "This division getting crazy.",
    "Best prospect alive.",
    "He needs better defense.",
    "UFC needs to sign him.",
    "This man different."
]


# =========================
# HANDLE SYSTEM
# =========================

def generate_handle(entity):
    # Keep existing handle if already set
    if "handle" in entity and entity["handle"]:
        return entity["handle"]

    # Use full name instead of first_name/last_name
    full_name = entity.get("name", "Unknown User")
    parts = full_name.split()

    first = parts[0].lower() if len(parts) > 0 else "user"
    last = parts[-1].lower() if len(parts) > 1 else str(random.randint(100, 999))

    choices = [
        f"{first}{last}",
        f"{first}_{last}",
        f"{first}.{last}",
        f"{last}{random.randint(1,999)}",
        f"{first}{random.randint(10,9999)}",
        f"real{first}",
        f"the{first}{last}"
    ]

    handle = "@" + random.choice(choices)

    entity["handle"] = handle
    return handle

# =========================
# POST CREATOR
# =========================

def create_post(author, category):
    if category == "fighter":
        content = random.choice(fighter_templates)
    else:
        content = random.choice(fan_templates)

    # Make sure handle exists
    if "handle" not in author:
        author["handle"] = generate_handle(author)

    post = {
        "author": author["name"],
        "handle": author["handle"],
        "verified": author.get("verified", False),
        "followers": author.get("followers", 0),
        "content": content,
        "likes": random.randint(0, 5000),
        "comments": random.randint(0, 800),
        "shares": random.randint(0, 400),
        "timestamp": str(datetime.now()),
        "category": category
    }

    cagewire_feed.append(post)
    return post


# =========================
# AUTO POST ENGINE
# =========================

def run_cagewire_cycle():
    fighters = world_entities["fighters"]
    fans = world_entities["fans"]

    generated_posts = []

    # Fighters post
    for fighter in fighters:
        if "handle" not in fighter:
            fighter["handle"] = generate_handle(fighter)

        activity_roll = random.randint(1, 100)

        if activity_roll <= fighter.get("social_media_activity", 50):
            generated_posts.append(create_post(fighter, "fighter"))

    # Fans post
    for fan in fans:
        if "handle" not in fan:
            fan["handle"] = generate_handle(fan)

        activity_roll = random.randint(1, 100)

        if activity_roll <= fan.get("social_media_activity", 30):
            generated_posts.append(create_post(fan, "fan"))

    return generated_posts


# =========================
# TRENDING SYSTEM
# =========================

def get_trending_posts():
    sorted_posts = sorted(
        cagewire_feed,
        key=lambda x: x["likes"] + x["comments"] + x["shares"],
        reverse=True
    )

    return sorted_posts[:20]


# =========================
# FEED VIEW
# =========================

def get_feed():
    return sorted(
        cagewire_feed,
        key=lambda x: x["timestamp"],
        reverse=True
    )
