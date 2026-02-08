from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


#USER SCHEMA
class UserBase(BaseModel):
    username: str = Field( min_length=5, max_length=20 )
    email: EmailStr = Field( max_length=120 )
    # password: str = Field( min_length=8 )
    

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_file: str | None
    image_path: str


# POST SCHEMA
class PostBase(BaseModel):
    # Without default values, these fields are required.
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: int # Temp placeholder

class PostUpdate(BaseModel):
    title: str | None = Field(min_length=1, max_length=100, default=None)
    content: str | None = Field(min_length=1, default=None)

class PostResponse(PostBase):
    # Allows pydantic to read dot notation
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse
    