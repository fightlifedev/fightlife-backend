import random

def injury_check(player):
    chance = random.randint(1, 100)

    if chance <= 10:
        player["injured"] = True
        player["injury_days_left"] = random.randint(3, 14)

    return player
