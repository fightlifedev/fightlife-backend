import random

social_graph = {}


def init_social(entity):
    handle = entity["handle"]

    if handle not in social_graph:
        social_graph[handle] = {
            "followers": entity.get("followers", random.randint(50, 5000)),
            "following": random.randint(20, 300),
            "friends": [],
            "rivals": []
        }


def follow(follower, target):
    init_social(follower)
    init_social(target)

    social_graph[target["handle"]]["followers"] += 1


def unfollow(follower, target):
    init_social(target)

    if social_graph[target["handle"]]["followers"] > 0:
        social_graph[target["handle"]]["followers"] -= 1


def get_social(entity):
    init_social(entity)
    return social_graph[entity["handle"]]
