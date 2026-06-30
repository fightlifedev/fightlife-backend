def recover_player(player):
    if player["fatigue"] > 0:
        player["fatigue"] -= 5

        if player["fatigue"] < 0:
            player["fatigue"] = 0

    if player["injured"]:
        player["injury_days_left"] -= 1

        if player["injury_days_left"] <= 0:
            player["injured"] = False
            player["injury_days_left"] = 0

    return player
