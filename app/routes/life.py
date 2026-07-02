from fastapi import APIRouter
from app.systems.life_engine import LifeEngine
from app.systems.choice_engine import generate_choice, resolve_choice
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
    
@router.get("/choice")
def get_choice():
    return generate_choice()


@router.post("/choice/{choice_id}/{decision}")
def make_choice(choice_id: int, decision: int):
    return resolve_choice(player, choice_id, decision)
