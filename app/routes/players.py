from fastapi import APIRouter

router = APIRouter(prefix="/players", tags=["Players"])

@router.get("/")
def get_players():
    return {"players": []}
