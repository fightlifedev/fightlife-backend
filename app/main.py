from fastapi import FastAPI
from app.routes.players import router as player_router
from app.routes.world import router as world_router
from app.routes import contracts

app = FastAPI()

app.include_router(player_router)
app.include_router(world_router)
app.include_router(contracts.router)

@app.get("/")
def root():
    return {"message": "FightLife API Running"}
