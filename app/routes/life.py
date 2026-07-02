from fastapi import APIRouter
from app.systems.life_engine import LifeEngine

router = APIRouter()

# temporary test player
player = {
    "name": "Devon Duffee",
    "age": 19,
    "day": 1,
    "month": 1,
    "year": 2026,
    "energy": 100,
    "money": 500,
    "stress": 0,
    "discipline": 50,
    "strength": 50,
    "skill": 50,
    "career": "fighter",
    "injured": False,
    "fame": 0
}

life = LifeEngine(player)


@router.post("/advance-day")
def advance_day():
    return life.advance_day()


@router.post("/train")
def train():
    return life.train()


@router.post("/work")
def work():
    return life.work_job()
