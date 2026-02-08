# ============================
# ========= Imports ==========
from fastapi import FastAPI, Request, HTTPException, status, Depends
# from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException as StarletteHTTPException # Built-in: For edge cases that HTTPExceptions might not catch.
from typing import List, Dict, Any, Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import PostCreate, PostResponse, UserCreate, UserResponse



# ===============================
# ========= Initialize ==========
Base.metadata.create_all(bind=engine)

server = FastAPI()
templates = Jinja2Templates(directory="templates")
server.mount("/static", StaticFiles(directory="static"), name="static")
server.mount("/media", StaticFiles(directory="media"), name="media")




# =========================
# ========= Data ==========





# ============================================
# ========= Template Page Functions ==========

# HOME PAGE AND ALL POSTS
@server.get("/", include_in_schema=False, name="home") 
@server.get("/posts", include_in_schema=False, name="posts") 
def home(request: Request, db: Annotated[Session, Depends(get_db)]):

    result = db.execute(select(models.Post))
    posts = result.scalars().all()

    context: dict = {
        "request": request,
        "posts": posts,
        "title": "Home"
    }

    return templates.TemplateResponse("home.html", context)



# route, don't show in docs, url name for url_for()
@server.get("/posts/{post_id}", include_in_schema=False)
def load_post(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):

    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()

    if post:
        title = post.title[:50]
        return templates.TemplateResponse("post.html", {"request": request, "post": post, "title": title})
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")




@server.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page( request: Request, user_id: int, db: Annotated[Session, Depends(get_db)] ):

    user_result = db.execute(select(models.User).where(models.User.id == user_id))
    user = user_result.scalars().first()

    if not user:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="User not found" )

    post_result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = post_result.scalars().all()

    context: dict = {
        "request": request,
        "posts": posts,
        "user": user,
        "title": f"{user.username}'s Posts"
    }

    return templates.TemplateResponse("user_posts.html", context)




# =========================================
# ========= Server API Functions ==========

# API CALL FOR USERS
@server.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user_result = db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = user_result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exists")

    email_result = db.execute(select(models.User).where(models.User.email == user.email))
    existing_email = email_result.scalars().first()

    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
    
    new_user = models.User(username = user.username, email = user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET SINGLE USER
@server.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):

    user_result = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = user_result.scalars().first()

    if existing_user:
        return existing_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")



# API CALL FOR ALL POSTS
@server.get("/api/posts/", response_model=list[PostResponse]) # response_model is out schema
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts



# API CALL FOR SINGLE POST
@server.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):

    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()

    if post:
        return post
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



# API FOR CREATING USER POST
@server.post( "/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="User not found" )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# API FOR GETTING ALL POSTS FROM SINGLE USER
@server.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):

    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="User not found" )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return posts




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
        "404.html",
        {
            "request": request,
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
        "404.html",
        {
            "request": request,
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )




# ======================================
# ========= Local State Check ==========
if __name__ == "__main__":
    pass
