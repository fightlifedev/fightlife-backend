import random


CHOICE_POOL = [
    {
        "id": 1,
        "event": "A local gym offers you a free week trial.",
        "choices": [
            "Join the gym",
            "Ignore it",
            "Ask for a longer free trial"
        ]
    },
    {
        "id": 2,
        "event": "A rival calls you out on CageWire.",
        "choices": [
            "Respond aggressively",
            "Ignore it",
            "Challenge them to fight"
        ]
    },
    {
        "id": 3,
        "event": "Your boss asks you to work overtime.",
        "choices": [
            "Accept overtime",
            "Decline",
            "Ask for a raise"
        ]
    },
    {
        "id": 4,
        "event": "Your partner says you spend too much time training.",
        "choices": [
            "Spend time together",
            "Keep training",
            "End the relationship"
        ]
    },
    {
        "id": 5,
        "event": "A promoter notices your recent performance.",
        "choices": [
            "Talk to them",
            "Ignore them",
            "Negotiate a deal"
        ]
    }
]


def generate_choice():
    return random.choice(CHOICE_POOL)


def resolve_choice(player, choice_id, decision):
    result = {}

    if choice_id == 1:
        if decision == 1:
            player["discipline"] += 5
            result["message"] = "You joined the gym and feel more focused."

        elif decision == 2:
            result["message"] = "You ignored the offer."

        elif decision == 3:
            player["charisma"] += 2
            result["message"] = "You negotiated more free time."

    elif choice_id == 2:
        if decision == 1:
            player["fame"] += 2
            player["stress"] += 2
            result["message"] = "Your aggressive response gains attention."

        elif decision == 2:
            result["message"] = "You ignored the callout."

        elif decision == 3:
            player["fame"] += 5
            result["message"] = "The fight hype is growing."

    elif choice_id == 3:
        player["money"] += random.randint(100, 300)
        result["message"] = "Extra money earned."

    elif choice_id == 4:
        player["happiness"] += 5
        result["message"] = "Relationship improved."

    elif choice_id == 5:
        player["fame"] += 10
        player["money"] += 500
        result["message"] = "Big opportunity unlocked."

    result["player"] = player
    return result
