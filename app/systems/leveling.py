def check_level_up(player):
    xp_needed = player["level"] * 100

    if player["xp"] >= xp_needed:
        player["level"] += 1
        player["xp"] -= xp_needed
        player["attribute_points"] += 1

    return player
