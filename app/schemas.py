from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from requests import post

from app.models import PostModel


# Schema, Pydantic Model
# 5:30:11
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

#Response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
     
    class Config:
        orm_mode = True
    
class Post(PostBase):
    id: int
    owner_id: int
    owner: UserResponse
    published_at: datetime

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    PostModel: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    delete_vote: bool = False