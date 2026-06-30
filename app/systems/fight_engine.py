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
        winner = "player"
    else:
        winner = "opponent"

    return {
        "winner": winner,
        "player_score": player_score,
        "opponent_score": opponent_score
    }
