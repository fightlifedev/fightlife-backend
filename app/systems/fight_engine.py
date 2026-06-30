import random


def simulate_fight(player, opponent):
    player_score = 0
    opponent_score = 0

    for round_num in range(3):
        player_round = (
            player["stats"]["boxing"]
            + player["stats"]["power"]
            + player["stats"]["cardio"]
            - player["fatigue"]
        )

        opponent_round = (
            opponent["stats"]["boxing"]
            + opponent["stats"]["power"]
            + opponent["stats"]["cardio"]
            - opponent["fatigue"]
        )

        player_roll = player_round + random.randint(1, 20)
        opponent_roll = opponent_round + random.randint(1, 20)

        if player_roll > opponent_roll:
            player_score += 1
        else:
            opponent_score += 1

    if player_score > opponent_score:
        winner = player
        loser = opponent
    else:
        winner = opponent
        loser = player

    # Fight method
    method_roll = random.randint(1, 100)

    if method_roll <= 20:
        method = "KO"
    elif method_roll <= 40:
        method = "Submission"
    else:
        method = "Decision"

    # Damage system
    winner_damage = random.randint(2, 8)
    loser_damage = random.randint(5, 15)

    winner["fatigue"] += winner_damage
    loser["fatigue"] += loser_damage

    # Injury chance
    injury_roll = random.randint(1, 100)

    if injury_roll <= 20:
        loser["injured"] = True
        loser["injury_days_left"] = random.randint(7, 30)

    # Record setup
    if "record" not in player:
        player["record"] = {"wins": 0, "losses": 0}

    if "record" not in opponent:
        opponent["record"] = {"wins": 0, "losses": 0}

    # Update record
    winner["record"]["wins"] += 1
    loser["record"]["losses"] += 1

    # XP gain
    if "xp" not in winner:
        winner["xp"] = 0

    winner["xp"] += random.randint(20, 50)

    # Reputation
    if "reputation" not in winner:
        winner["reputation"] = 0

    winner["reputation"] += random.randint(5, 15)

    # Payout
    purse = 0
    if "scheduled_fight" in player:
        purse = player["scheduled_fight"].get("purse", 0)

    winner["money"] = winner.get("money", 0) + purse

    # Clear camp
    player["fight_camp"] = {
        "active": False,
        "opponent": None,
        "days_left": 0,
        "weight_cut": None,
        "peak": False
    }

    # Clear scheduled fight
    player["scheduled_fight"] = {
        "opponent": None,
        "days_until_fight": 0,
        "purse": 0,
        "accepted": False,
        "completed": True
    }

    return {
        "winner": winner["name"],
        "method": method,
        "player_score": player_score,
        "opponent_score": opponent_score,
        "winner_record": winner["record"],
        "loser_record": loser["record"],
        "winner_reputation": winner.get("reputation", 0),
        "winner_money": winner.get("money", 0)
    }
