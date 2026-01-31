from fastapi import FastAPI, Request, HTTPException, status
# from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException # Built-in: For edge cases that HTTPExceptions might not catch.
from typing import List, Dict, Any


# ===============================
# ========= Initialize ==========
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


# ==========================================
# ========= Server Page Functions ==========

# HOME PAGE AND ALL POSTS
@server.get("/", include_in_schema=False, name="home") 
@server.get("/posts", include_in_schema=False, name="posts") 
def home(req: Request):

    context = {
        "posts": posts,
        "title": "home"
    }
    return templates.TemplateResponse(req, "home.html", context)


# route, don't show in docs, url name for url_for()
@server.get("/posts/{post_id}", include_in_schema=False)
def load_post(req: Request, post_id: int):

    for post in posts:
        if post.get("id") == post_id:
            context: dict = {"post": post, "title": post["title"][:50] }
            return templates.TemplateResponse(req, "post.html", context)
    
    return templates.TemplateResponse(req, "404.html", {"status_code": status.HTTP_404_NOT_FOUND, "message": "Sorry but the page you are looking for has moved or does not exist. "})




# =========================================
# ========= Server API Functions ==========

# API CALL FOR POSTS
@server.get("/api/posts/")
def get_posts():
    return posts


@server.get("/api/posts/{post_id}")
def get_post(post_id: int):

    for post in posts:
        print(post.get("id"))
        if post.get("id") == post_id:
            return post
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")




# ==========================================
# ========= Server Error Handling ==========

## StarletteHTTPException Handler
@server.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "404.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@server.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "404.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


if __name__ == "__main__":
    pass
