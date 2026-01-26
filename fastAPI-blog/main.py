from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any

server = FastAPI()
templates = Jinja2Templates(directory="templates")
server.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# ========= Data ==========
posts: List[Dict[str, Any]] = [
    {
        "id": 1,
        "author": "Eric Philippot",
        "title": "Mario Bros. 3 Was The Best!",
        "content": "Mario Bros 3 improved on the original in so many ways, with new power ups, many unique enemies and fun themes.",
        "date_posted": "2026-01-24"
    },
    {
        "id": 2,
        "author": "John Doe",
        "title": "The Glory of Pac-Man",
        "content": "Pac-Man revolutionized arcade gaming with its simple yet addictive gameplay, chasing dots and avoiding ghosts in a maze.",
        "date_posted": "2023-05-10"
    },
    {
        "id": 3,
        "author": "Jane Smith",
        "title": "Why Tetris is Timeless",
        "content": "Tetris's puzzle mechanics have stood the test of time, challenging players to arrange falling blocks in endless combinations.",
        "date_posted": "2023-06-15"
    },
    {
        "id": 4,
        "author": "Bob Johnson",
        "title": "Sonic the Hedgehog's Speed Run",
        "content": "Sonic's fast-paced platforming on the Sega Genesis captured the essence of speed and adventure in retro gaming.",
        "date_posted": "2023-07-20"
    },
    {
        "id": 5,
        "author": "Alice Brown",
        "title": "Zelda's Adventure on NES",
        "content": "The Legend of Zelda on NES introduced epic exploration, puzzles, and swordplay that defined adventure games.",
        "date_posted": "2023-08-25"
    }
]


# =====================================
# ========= Server Functions ==========
@server.get("/", include_in_schema=False, name="home") 
@server.get("/posts", include_in_schema=False, name="posts") 
def home(req: Request):
    context = {
        "posts": posts,
        "title": "home"
    }
    return templates.TemplateResponse(req, "home.html", context)

@server.get("/api/posts")
def get_posts() -> List[Dict[str, Any]]:
    return posts


if __name__ == "__main__":
    pass
