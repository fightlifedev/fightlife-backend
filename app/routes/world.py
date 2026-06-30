from fastapi import APIRouter

router = APIRouter(prefix="/world", tags=["World"])

@router.get("/")
def get_world():
    return {"world": "FightLife world loaded"}
