import random
from app.routes.players import players


# =========================
# LIFE EVENT POOL
# =========================

life_event_pool = [
    "minor_injury",
    "major_injury",
    "sponsorship_offer",
    "gym_conflict",
    "mental_breakdown",
    "family_issue",
    "legal_trouble",
    "media_attention",
    "fan_growth",
    "relationship_drama",
    "unexpected_money",
    "burnout",
    "motivation_boost",
    "training_breakthrough",
    "coach_leaves",
    "nothing"
]


# =========================
# LIFE EVENT ENGINE
# =========================

def trigger_life_event(player_name: str):
    fighter = players[player_name]

    event = random.choice(life_event_pool)

    # MINOR INJURY
    if event == "minor_injury":
        fighter["health"]["injured"] = True
        fighter["health"]["injury_type"] = "Minor Injury"
        fighter["health"]["recovery_days"] = random.randint(3, 14)

        fighter["memory"].append(
            "Suffered a minor injury."
        )

        return {
            "event": "Minor injury occurred"
        }

    # MAJOR INJURY
    elif event == "major_injury":
        fighter["health"]["injured"] = True
        fighter["health"]["injury_type"] = "Major Injury"
        fighter["health"]["recovery_days"] = random.randint(30, 180)

        fighter["career"]["active"] = False

        fighter["memory"].append(
            "Career paused due to major injury."
        )

        return {
            "event": "Major injury occurred"
        }

    # SPONSORSHIP
    elif event == "sponsorship_offer":
        money = random.randint(1000, 15000)

        fighter["finances"]["cash"] += money
        fighter["reputation"]["industry"] += 2

        fighter["memory"].append(
            f"Received sponsorship worth ${money}."
        )

        return {
            "event": "Sponsorship secured"
        }

    # GYM CONFLICT
    elif event == "gym_conflict":
        fighter["morale"] -= 5

        fighter["memory"].append(
            "Had conflict at the gym."
        )

        return {
            "event": "Gym conflict"
        }

    # MENTAL BREAKDOWN
    elif event == "mental_breakdown":
        fighter["mental"]["stability"] -= 15
        fighter["morale"] -= 10

        fighter["memory"].append(
            "Experienced mental breakdown."
        )

        return {
            "event": "Mental health declined"
        }

    # FAMILY ISSUES
    elif event == "family_issue":
        fighter["morale"] -= 8

        fighter["memory"].append(
            "Family issues affected focus."
        )

        return {
            "event": "Family issue"
        }

    # LEGAL TROUBLE
    elif event == "legal_trouble":
        fighter["career"]["active"] = False

        jail_days = random.randint(7, 365)

        fighter["memory"].append(
            f"Arrested. Out for {jail_days} days."
        )

        return {
            "event": "Legal trouble"
        }

    # MEDIA ATTENTION
    elif event == "media_attention":
        rep_gain = random.randint(2, 8)

        fighter["reputation"]["industry"] += rep_gain
        fighter["followers"] += random.randint(500, 5000)

        fighter["memory"].append(
            "Gained media attention."
        )

        return {
            "event": "Media buzz increased"
        }

    # FAN GROWTH
    elif event == "fan_growth":
        fans = random.randint(1000, 10000)

        fighter["followers"] += fans

        fighter["memory"].append(
            f"Gained {fans} followers."
        )

        return {
            "event": "Fanbase grew"
        }

    # RELATIONSHIP DRAMA
    elif event == "relationship_drama":
        fighter["morale"] -= 8
        fighter["mental"]["stability"] -= 5

        fighter["memory"].append(
            "Relationship drama caused stress."
        )

        return {
            "event": "Relationship issues"
        }

    # RANDOM MONEY
    elif event == "unexpected_money":
        money = random.randint(500, 25000)

        fighter["finances"]["cash"] += money

        fighter["memory"].append(
            f"Unexpectedly received ${money}."
        )

        return {
            "event": "Unexpected income"
        }

    # BURNOUT
    elif event == "burnout":
        fighter["energy"] -= 15
        fighter["morale"] -= 10

        fighter["memory"].append(
            "Feeling burned out."
        )

        return {
            "event": "Burnout"
        }

    # MOTIVATION BOOST
    elif event == "motivation_boost":
        fighter["morale"] += 10
        fighter["energy"] += 10

        fighter["memory"].append(
            "Feeling highly motivated."
        )

        return {
            "event": "Motivation boost"
        }

    # TRAINING BREAKTHROUGH
    elif event == "training_breakthrough":
        stat_gain = random.randint(1, 3)

        fighter["attributes"]["power"] += stat_gain
        fighter["attributes"]["speed"] += stat_gain

        fighter["memory"].append(
            "Made a training breakthrough."
        )

        return {
            "event": "Training breakthrough"
        }

    # COACH LEAVES
    elif event == "coach_leaves":
        fighter["morale"] -= 7

        fighter["memory"].append(
            "Coach left the gym."
        )

        return {
            "event": "Coach departure"
        }

    # NORMAL DAY
    else:
        fighter["memory"].append(
            "Nothing major happened today."
        )

        return {
            "event": "Normal day"
        }
