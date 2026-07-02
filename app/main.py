from fastapi import FastAPI
from app.routes.life import router as life_router
from app.routes.players import router as player_router
from app.routes.world import router as world_router
from app.routes import contracts
from app.routes import cagewire

app = FastAPI()

# ============================
# ROUTERS
# ============================

app.include_router(player_router)
app.include_router(world_router)
app.include_router(contracts.router)
app.include_router(cagewire.router)
app.include_router(life_router, prefix="/life", tags=["Life"])

# ============================
# ROOT
# ============================

@app.get("/")
def root():
    return {
        "message": "FightLife API Running"
    }
