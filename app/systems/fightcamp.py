def start_fight_camp(player, opponent, days_until_fight):
    player["fight_camp"] = {
        "active": True,
        "opponent": opponent,
        "days_left": days_until_fight,
        "intensity": "medium",
        "weight_cut": 0,
        "peak": False
    }

    return player


def advance_fight_camp(player):
    if "fight_camp" not in player:
        return player

    if not player["fight_camp"]["active"]:
        return player

    player["fight_camp"]["days_left"] -= 1

    if player["fight_camp"]["days_left"] <= 7:
        player["fight_camp"]["peak"] = True

    if player["fight_camp"]["days_left"] <= 0:
        player["fight_camp"]["active"] = False

    return player
