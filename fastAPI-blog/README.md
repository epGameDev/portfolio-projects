# FastAPI Blog — Full Educational Walkthrough

This document is a hands-on, from-scratch rebuild guide and deep explanation of the FastAPI blog in this repository. It assumes only Python basics. You will learn FastAPI routing, Pydantic v2 schemas, modern SQLAlchemy 2.0 ORM, Jinja2 templating, static/media serving, and error handling. Each section explains the “how” and the “why,” with code you can paste to recreate the project, plus trade-offs and alternatives so you understand the design, not just copy it.

Status (validated against current code on 2026-02-07):
- Python ≥ 3.14
- FastAPI 0.128.0, Starlette 0.50.0
- SQLAlchemy 2.0.46
- Pydantic 2.12.5
- SQLite file DB: blog.db

--------------------------------------------------------------------------------
## 1) Project Structure

- [database.py](database.py) — Engine, session factory, `Base`, and `get_db()` dependency (why: creates a clean per-request DB session boundary and a single source of truth for DB config).
- [models.py](models.py) — SQLAlchemy ORM models: `User`, `Post`, relationships (why: one place defines schema + relations used by both API and templates).
- [schemas.py](schemas.py) — Pydantic v2 schemas for request/response shapes (why: validate input, shape output, and decouple external contract from internal ORM objects).
- [main.py](main.py) — FastAPI app, routes (HTML + JSON), error handlers, static/media mounts (why: wiring layer that composes dependencies, views, and responses).
- templates/ — Jinja2 templates (see [templates/layout.html](templates/layout.html), [templates/home.html](templates/home.html)) (why: server-rendered pages reuse the same data the API produces).
- static/ — CSS, images, manifest (served at `/static`) (why: asset pipeline kept simple for learning).
- media/ — user-uploaded profile pictures (served at `/media`) (why: separates user content from code and static assets).

--------------------------------------------------------------------------------
## 2) Set Up the Environment

Using `uv` (modern Python project manager):

```bash
# Install dependencies from pyproject.toml
uv sync
```

**Why this matters:**
- **uv**: Replaces pip, venv, and poetry. `uv sync` reads `pyproject.toml`, creates a virtual environment if missing, and creates/updates a lockfile (`uv.lock`) for reproducible builds.
- **FastAPI**: Provides routing + DI; Starlette (under the hood) runs the ASGI server pieces.
- **SQLAlchemy 2.0**: The modern declarative ORM; sticking to 2.0 APIs avoids legacy patterns.
- **Pydantic v2**: Validates inputs and serializes outputs; `from_attributes` lets you return ORM objects directly.
- **SQLite**: Zero-setup; swap the URL later for Postgres without changing the app code.

--------------------------------------------------------------------------------
## 3) Database Layer (`database.py`)

**Goal**: Establish a connection to the database and a way to get a "session" (transaction) for each request.

**Concept**: A "Session" is a workspace for your objects. You load objects into it, modify them, and then "commit" to save changes to the real database. We need a new session for every HTTP request to keep them isolated (thread-safety).

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# 1. Create the engine (the connection pool)
# check_same_thread=False is ONLY for SQLite, because it thinks single-thread by default
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# 2. Create the Session Factory
# autocommit=False: We want to control when we save.
# autoflush=False: We want to control when SQL is sent.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a Base class for our Models to inherit from
class Base(DeclarativeBase):
    pass

# 4. Dependency to use in our endpoints
def get_db():
    with SessionLocal() as db:
        yield db
```

**What is specific code doing?**
- `create_engine`: Sets up the connection pool. It doesn't connect immediately, but prepares the way.
- `connect_args={"check_same_thread": False}`: **CRITICAL for SQLite in FastAPI**. FastAPI runs requests in different threads. SQLite forbids this by default. This flag turns off that check.
- `SessionLocal`: This is a *factory*. We act like it's a class we can instantiate (`db = SessionLocal()`).
- `with SessionLocal() as db`: Best practice for resource management. It automatically closes the session when the block exits (even if errors occur).
- `yield db`: When FastAPI calls this dependency, it pauses here. The route runs. When the route finishes, it resumes and the `with` block closes the session.

**Alternatives/Design Choices:**
- **Why not global session?** If two requests use the same session, one might commit the other's half-finished data. Bad!
- **Postgres?** Just change the URL strings. The `SessionLocal` and code patterns remain identical.

--------------------------------------------------------------------------------
## 4) ORM Models (`models.py`)

**Goal**: Define the structure of our tables (Users and Posts).

**Concept**: "Code First" database design. We define Python classes, and SQLAlchemy tells the database to create tables that match.

```python
from __future__ import annotations 
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Mapped[...] is the SQLAlchemy 2.0 way to type hint
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    # Relationship: Not a real column. Lets us do user.posts in Python.
    posts: Mapped[list[Post]] = relationship(back_populates="author")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pictures/{self.image_file}"
        return "/static/images/default.jpg"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # ForeignKey: This IS a real column. It stores the integer ID of the user.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # Relationship: Lets us do post.author in Python.
    author: Mapped[User] = relationship(back_populates="posts")
```

**What is specific code doing?**
- `Mapped[int]`: Tells type checkers (and IDEs) this is an integer.
- `mapped_column`: Defines the actual SQL column rules (Primary Key, Nullable, etc).
- `relationship`: Magic. It tells SQLAlchemy to run a secondary query or JOIN when we access this property. 
- `back_populates`: Syncs the two sides. If you add a post to `user.posts`, SQLAlchemy automatically sets `post.author` to that user.

**Alternatives/Design Choices:**
- **Why `__future__`?** Allows us to use `Post` inside `User` before `Post` is defined.
- **Why `lazy="selectin"` (Optional)?** You might see this recommended. It tells SQLAlchemy to load relationships automatically (Eager Loading) to prevent errors if you try to access data after the session closes.

--------------------------------------------------------------------------------
## 5) Schemas (Pydantic v2) (`schemas.py`)

**Goal**: Define the "Contract" for our API. What data do we accept? What data do we return?

**Concept**: ORM models (`models.py`) are for the database (everything included). Schemas are for the user (sensitive info hidden, data formatted). We map between them.

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

# Base: Shared properties
class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)

# Input: What the user sends to create an account
class UserCreate(UserBase):
    pass

# Output: What we send back to the user
class UserResponse(UserBase):
    # ConfigDict(from_attributes=True) is MAGIC. 
    # It tells Pydantic: "I know this expects a dict, but if I give you an Object (like ORM), just read the attributes (obj.id) instead of keys (obj['id'])."
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_file: str | None
    image_path: str

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

class PostCreate(PostBase):
    user_id: int

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    date_posted: datetime
    # Nested Schema! This will automatically convert the ORM user object into the UserResponse format.
    author: UserResponse
```

**What is specific code doing?**
- `Field(...)`: Adds validation rules. FastAPI handles the error messages for you if these rules are broken.
- `from_attributes=True`: Previously called `orm_mode`. This is the bridge. It allows `UserResponse(id=1)` to be created from `user_orm_obj` where `user_orm_obj.id == 1`.
- `author: UserResponse`: This is powerful. When we return a Post, Pydantic sees the `author` relationship, grabs that User object, and runs it through `UserResponse` automatically.

**Alternatives/Design Choices:**
- **Sensitive Data**: We are currently inheriting `UserBase` in `UserResponse`, which INCLUDES the password field. **Security Tip**: In a real app, `UserResponse` should NOT inherit `password`. We would define a separate base or explicit fields to exclude it.

--------------------------------------------------------------------------------
## 6) Application (`main.py`)

**Goal**: Tie everything together. Define routes (URLs) and connect them to database actions.

**Concept**: A "Dependency Injection" system is used (`Depends`). We don't manually create connections. We ask for them.

```python
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated

import models
from database import Base, engine, get_db
from schemas import PostCreate, PostResponse, UserCreate, UserResponse

# Create the tables in the DB if they don't exist
Base.metadata.create_all(bind=engine)

server = FastAPI()

# Mount folders to URLs
server.mount("/static", StaticFiles(directory="static"), name="static")
server.mount("/media", StaticFiles(directory="media"), name="media")

# Setup Jinja2
templates = Jinja2Templates(directory="templates")

# Dependency Shortcut: Annotated lets us just write `db: Session` in endpoints later
DbSession = Annotated[Session, Depends(get_db)]

# -------- HTML Routes (Return TemplateResponse) --------

@server.get("/", include_in_schema=False, name="home")
def home(request: Request, db: DbSession):
    # Query: Select all posts
    # scalars(): Get the objects (Post), not the Row result tuples
    # all(): Fetch them list
    posts = db.execute(select(models.Post)).scalars().all()
    
    # Context: Data passed to the HTML template
    # 'request': REQUIRED for url_for to work
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "title": "Home"})


@server.get("/posts/{post_id}", include_in_schema=False)
def load_post(request: Request, post_id: int, db: DbSession):
    # Query: Select Post where id matches
    post = db.execute(select(models.Post).where(models.Post.id == post_id)).scalars().first()
    
    if not post:
        # Standard HTTP 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    return templates.TemplateResponse("post.html", {"request": request, "post": post, "title": post.title})


# -------- JSON API Routes (Return Pydantic Models) --------

@server.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: DbSession):
    # 1. Validation Logic
    if db.execute(select(models.User).where(models.User.username == user.username)).scalars().first():
        raise HTTPException(status_code=400, detail="Username taken")
    
    # 2. Create ORM Object (converting from Pydantic schema)
    new_user = models.User(username=user.username, email=user.email)
    
    # 3. Add to Session -> Commit -> Refresh
    # Add: Put in workspace
    # Commit: Save to DB (Obtain ID)
    # Refresh: Update our object with the new ID and default values (like dates)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@server.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: DbSession):
    # Pydantic Magic: We return a list of ORM objects. 
    # FastAPI sees `response_model=list[PostResponse]`.
    # It loops through, and converts each ORM object to the Schema automatically.
    return db.execute(select(models.Post)).scalars().all()
```

**What is specific code doing?**
- `response_model=...`: This is the most important part of the API. It tells FastAPI "Filter the data using this Schema before sending it to the user". If your DB object has a `password` field but your Schema doesn't, it is removed here.
- `Depends(get_db)`: When the request starts, `get_db` opens a session. When the function finishes, `get_db` closes it.

--------------------------------------------------------------------------------
## 7) Templates (Jinja2) using Relationships

**Goal**: Display data in HTML.

**Concept**: Jinja2 is a templating language. It lets us write python-like code inside HTML.

```html
<!-- templates/home.html -->
{% extends "layout.html" %}

{% block content %}
  {% for post in posts %}
    <!-- Relationship Access: post.author triggers a DB lookup or uses loaded data -->
    <h3>{{ post.title }} by {{ post.author.username }}</h3>
    
    <!-- url_for: Generates the URL for a function name. 
         If we change the URL in main.py, this updates automatically. -->
    <a href="{{ url_for('load_post', post_id=post.id) }}">Read More</a>
  {% endfor %}
{% endblock %}
```

**Pitfall Warning**: `url_for` requires the *argument names* to match the path parameters in `main.py`. If existing code had `href="{{ url_for(...), user_id=... }}"` (comma outside), that is invalid Python syntax. It must be `url_for(..., user_id=...)`.

--------------------------------------------------------------------------------
## 8) Running the Server

```bash
uv run uvicorn main:server --reload
```

- **uv run**: Runs the command inside the project's virtual environment automatically.
- **uvicorn**: The ASGI server.
- **main:server**: Look in `main.py` for the variable `server`.
- **--reload**: Watch files and restart if code changes (Dev only).

--------------------------------------------------------------------------------
## 9) Common Pitfalls & "Gotchas"

1.  **"Detached Instance Error"**:
    *   *Symptom*: You try to access `post.author` in the template, but the request has already finished and the DB session is closed.
    *   *Why*: SQLAlchemy lazy-loads by default. It tries to go back to the DB to get the author, but the connection is gone.
    *   *Fix 1 (Global)*: In `database.py`, set `expire_on_commit=False` in `SessionLocal`. This strictly separates the object lifecycle from the transaction scope.
    *   *Fix 2 (Query-Level)*: In your query, use `.options(selectinload(Post.author))`. This is often preferred for performance as it fetches everything in one go (Eager Loading).

2.  **Path Parameter Types**:
    *   *Symptom*: `AssertionError: Path params must be of one of the supported types`.
    *   *Why*: You wrote `def get_user(user_id: UserResponse)`. FastAPI thinks you want to parse the *URL* into a whole Object.
    *   *Fix*: Path params must be simple types. Use `def get_user(user_id: int)`.

3.  **Template url_for Error**:
    *   *Symptom*: `TemplateSyntaxError`.
    *   *Why*: Incorrect parenthesis placement.
    *   *Fix*: `{{ url_for('name', arg=value) }}`.

--------------------------------------------------------------------------------
## 10) Extension Ideas

1.  **Add Pagination**:
    *   Change `get_posts` to accept `skip: int = 0, limit: int = 10`.
    *   Update query: `select(models.Post).offset(skip).limit(limit)`.
2.  **Secure Passwords**:
    *   Install `passlib[bcrypt]`.
    *   Hash `new_user.password` before adding to DB.
    *   Remove `password` from `UserResponse` schema.
