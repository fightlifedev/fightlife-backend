from fastapi import FastAPI
from routes.players import router as player_router
from routes.world import router as world_router

app = FastAPI()

app.include_router(player_router)
app.include_router(world_router)


@app.get("/")
def root():
    return {"message": "FightLife API Running"}
