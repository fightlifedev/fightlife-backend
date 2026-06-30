from fastapi import APIRouter
from app.database import players_collection

router = APIRouter()

@router.post("/players")
def create_player(player: dict):
    result = players_collection.insert_one(player)
    return {
        "message": "Player created",
        "player_id": str(result.inserted_id)
    }

@router.get("/players")
def get_players():
    players = list(players_collection.find({}, {"_id": 0}))
    return players
