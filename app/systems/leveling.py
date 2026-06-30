def level_up_check(player):
    xp_needed = player["level"] * 100

    if player["xp"] >= xp_needed:
        player["xp"] -= xp_needed
        player["level"] += 1
        player["potential"] += 1

    return player
