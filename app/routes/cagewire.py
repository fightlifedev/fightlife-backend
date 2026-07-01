from fastapi import APIRouter
from app.systems.cagewire_engine import (
    generate_random_post,
    get_feed
)

router = APIRouter()


# ============================
# GENERATE A NEW POST
# ============================

@router.post("/cagewire/generate-post")
def create_post():
    post = generate_random_post()

    if not post:
        return {
            "message": "No post generated"
        }

    return {
        "message": "Post created",
        "post": post
    }


# ============================
# VIEW LIVE FEED
# ============================

@router.get("/cagewire/feed")
def view_feed():
    return {
        "feed": get_feed()
    }


# ============================
# BULK GENERATE POSTS
# ============================

@router.post("/cagewire/generate-bulk/{amount}")
def generate_bulk(amount: int):
    posts = []

    for _ in range(amount):
        post = generate_random_post()

        if post:
            posts.append(post)

    return {
        "message": f"{amount} posts generated",
        "posts": posts
    }
