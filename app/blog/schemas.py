from pydantic import BaseModel
from typing import List, Optional


class BaseBlog(BaseModel):
    title: str
    body: str


class Blog(BaseBlog):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUserInBlog(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(ShowUserInBlog):
    blogs: List[Blog] = []


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUserInBlog = None

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

