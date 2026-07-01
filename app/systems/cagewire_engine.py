import random
from datetime import datetime, timedelta

cagewire_feed = []

# ==========================
# ENTITY DATABASE (TEST)
# ==========================

entities = [
    {
        "first_name": "Conor",
        "last_name": "McGregor",
        "type": "fighter",
        "followers": 46000000,
        "verified": True,
        "activity": 0.85,
        "emotion": "confident"
    },
    {
        "first_name": "Islam",
        "last_name": "Makhachev",
        "type": "fighter",
        "followers": 9200000,
        "verified": True,
        "activity": 0.65,
        "emotion": "focused"
    },
    {
        "first_name": "Dana",
        "last_name": "White",
        "type": "promoter",
        "followers": 8100000,
        "verified": True,
        "activity": 0.40,
        "emotion": "neutral"
    },
    {
        "first_name": "Jake",
        "last_name": "MMAFan",
        "type": "fan",
        "followers": 843,
        "verified": False,
        "activity": 0.75,
        "emotion": "excited"
    }
]

# ==========================
# POST TEMPLATES
# ==========================

fighter_posts = [
    "Big fight news soon.",
    "Nobody can stop me.",
    "Camp going crazy.",
    "Respect to my opponent.",
    "Focused."
]

fan_posts = [
    "That fight was insane.",
    "He got robbed.",
    "Future champ right there.",
    "Best fighter alive."
]

promoter_posts = [
    "Huge announcement soon.",
    "Contracts being finalized.",
    "Big things coming."
]

# ==========================
# HANDLE GENERATOR
# ==========================

def generate_handle(entity):
    return f"@{entity['first_name'].lower()}.{entity['last_name'].lower()}"

# ==========================
# TIMESTAMP ENGINE
# ==========================

def generate_dynamic_timestamp():
    minutes_ago = random.randint(1, 1440)
    return str(datetime.now() - timedelta(minutes=minutes_ago))

# ==========================
# ENGAGEMENT ENGINE
# ==========================

def generate_engagement(followers):
    likes = random.randint(
        max(5, int(followers * 0.001)),
        max(50, int(followers * 0.03))
    )

    comments = random.randint(
        max(1, int(likes * 0.05)),
        max(2, int(likes * 0.25))
    )

    shares = random.randint(
        max(1, int(likes * 0.01)),
        max(2, int(likes * 0.10))
    )

    return likes, comments, shares

# ==========================
# SHOULD POST?
# ==========================

def should_post(entity):
    return random.random() < entity["activity"]

# ==========================
# CREATE POST
# ==========================

def create_post(entity):
    if entity["type"] == "fighter":
        content = random.choice(fighter_posts)
    elif entity["type"] == "fan":
        content = random.choice(fan_posts)
    else:
        content = random.choice(promoter_posts)

    likes, comments, shares = generate_engagement(entity["followers"])

    post = {
        "author": f"{entity['first_name']} {entity['last_name']}",
        "handle": generate_handle(entity),
        "verified": entity["verified"],
        "followers": entity["followers"],
        "content": content,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "timestamp": generate_dynamic_timestamp(),
        "category": entity["type"]
    }

    cagewire_feed.append(post)

    return post

# ==========================
# MAIN CYCLE
# ==========================

def run_cagewire_cycle():
    new_posts = []

    for entity in entities:
        if should_post(entity):
            new_posts.append(create_post(entity))

    return new_posts

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
    return sorted(
        cagewire_feed,
        key=lambda x: x["likes"] + x["comments"] + x["shares"],
        reverse=True
    )[:10]
