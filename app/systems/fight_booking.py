def book_fight(player, opponent, days_until_fight, purse):
    player["scheduled_fight"] = {
        "opponent": opponent,
        "days_until_fight": days_until_fight,
        "purse": purse,
        "accepted": True,
        "completed": False
    }

    return player


def advance_fight_booking(player):
    if "scheduled_fight" not in player:
        return player

    if player["scheduled_fight"]["completed"]:
        return player

    player["scheduled_fight"]["days_until_fight"] -= 1

    if player["scheduled_fight"]["days_until_fight"] < 0:
        player["scheduled_fight"]["days_until_fight"] = 0

    return player
