import random

COMMENT_POOL = [
    "He not ready 😭",
    "This fight would be crazy",
    "Book it now",
    "You getting slept",
    "Big cap 😂",
    "Nah he serious",
    "This gone be war",
    "He calling him out fr",
    "We need this fight",
    "He better respond"
]


def generate_comments(post, world_entities):
    comments_feed = []

    comment_count = random.randint(2, 8)

    for _ in range(comment_count):
        commenter = random.choice(world_entities)

        comments_feed.append({
            "author": commenter["handle"],
            "content": random.choice(COMMENT_POOL)
        })

    return comments_feed
