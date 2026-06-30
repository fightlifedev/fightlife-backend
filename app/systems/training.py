import random

def train_player(player, skill):
    xp_gain = random.randint(10, 30)
    fatigue_gain = random.randint(2, 5)

    player["xp"] += xp_gain
    player["fatigue"] += fatigue_gain

    if skill in player["stats"]:
        player["stats"][skill] += 1

    return player
