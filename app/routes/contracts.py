from fastapi import APIRouter
import random
from app.routes.players import players

router = APIRouter()

# =========================
# PROMOTIONS DATABASE
# =========================

promotions = {
    "UFC": {
        "tier": 1,
        "min_reputation": 40,
        "min_amateur_wins": 10,
        "base_contract": 50000
    },

    "Bellator": {
        "tier": 2,
        "min_reputation": 25,
        "min_amateur_wins": 6,
        "base_contract": 20000
    },

    "PFL": {
        "tier": 2,
        "min_reputation": 20,
        "min_amateur_wins": 5,
        "base_contract": 15000
    },

    "LFA": {
        "tier": 3,
        "min_reputation": 10,
        "min_amateur_wins": 3,
        "base_contract": 5000
    }
}

# =========================
# ACTIVE CONTRACT OFFERS
# =========================

contract_offers = {}

# =========================
# SCOUTING SYSTEM
# =========================

def evaluate_fighter_for_contract(player_name: str):
    fighter = players[player_name]

    if fighter["career"]["contracted"]:
        return None

    amateur_wins = fighter["career"]["amateur_record"]["wins"]
    reputation = fighter["reputation"]["industry"]
    potential = fighter["attributes"]["potential"]

    possible_offers = []

    for promotion_name, promotion in promotions.items():
        if (
            amateur_wins >= promotion["min_amateur_wins"]
            and reputation >= promotion["min_reputation"]
        ):
            possible_offers.append(promotion_name)

    if not possible_offers:
        return None

    chosen_promotion = random.choice(possible_offers)

    contract_value = (
        promotions[chosen_promotion]["base_contract"]
        + (potential * 250)
    )

    offer = {
        "promotion": chosen_promotion,
        "value": contract_value,
        "fights": random.randint(2, 6),
        "accepted": False
    }

    contract_offers[player_name] = offer

    return offer

# =========================
# ROUTES
# =========================

@router.post("/evaluate-contract/{player_name}")
def evaluate_contract(player_name: str):
    if player_name not in players:
        return {"error": "Player not found"}

    offer = evaluate_fighter_for_contract(player_name)

    if not offer:
        return {
            "message": f"{player_name} has no offers yet"
        }

    return {
        "message": "Contract offer received",
        "offer": offer
    }


@router.post("/accept-contract/{player_name}")
def accept_contract(player_name: str):
    if player_name not in contract_offers:
        return {
            "error": "No contract offer available"
        }

    fighter = players[player_name]
    offer = contract_offers[player_name]

    fighter["career"]["contracted"] = True
    fighter["career"]["league"] = offer["promotion"]
    fighter["career"]["status"] = "Professional"

    fighter["finances"]["cash"] += offer["value"]

    fighter["memory"].append(
        f"Signed with {offer['promotion']} for ${offer['value']}"
    )

    offer["accepted"] = True

    return {
        "message": f"{player_name} signed with {offer['promotion']}",
        "contract": offer,
        "fighter": fighter
    }


@router.post("/decline-contract/{player_name}")
def decline_contract(player_name: str):

    if players[player_name]["career"]["contracted"]:
        return {
            "message": f"{player_name} is already signed and cannot decline."
        }

    if player_name not in contract_offers:
        return {
            "message": "No active contract offer found."
        }

    fighter = players[player_name]
    offer = contract_offers[player_name]

    fighter["memory"].append(
        f"Declined contract from {offer['promotion']}"
    )

    del contract_offers[player_name]

    return {
        "message": f"{player_name} declined the contract"
    }


@router.get("/contract-offers/{player_name}")
def get_contract_offer(player_name: str):

    if player_name not in contract_offers:
        return {
            "message": "No active contract offers"
        }

    return contract_offers[player_name]
