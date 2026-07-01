from fastapi import APIRouter
from app.systems.cagewire_engine import (
    run_cagewire_cycle,
    get_feed,
    get_trending_posts
)

router = APIRouter(prefix="/cagewire", tags=["CageWire"])


# Generate new CageWire cycle
@router.post("/generate-post")
def generate_posts():
    posts = run_cagewire_cycle()

    return {
        "message": "CageWire cycle generated",
        "posts": posts
    }


# Full feed
@router.get("/feed")
def fetch_feed():
    return {
        "feed": get_feed()
    }


# Trending posts
@router.get("/trending")
def fetch_trending():
    return {
        "trending": get_trending_posts()
    }
