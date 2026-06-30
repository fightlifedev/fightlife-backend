import random
from app.systems.leveling import level_up_check

def train_player(player, skill):
    xp_gain = random.randint(10, 30)
    fatigue_gain = random.randint(2, 5)

    player["xp"] += xp_gain
    player["fatigue"] += fatigue_gain

    if skill in player["stats"]:
        player["stats"][skill] += 1

    if "level" not in player:
        player["level"] = 1

    if "potential" not in player:
        player["potential"] = 50

    level_up_check(player)

    return {
        "xp_gain": xp_gain,
        "fatigue_gain": fatigue_gain,
        "current_xp": player["xp"],
        "current_level": player["level"],
        "updated_stat": player["stats"].get(skill, None)
    }
