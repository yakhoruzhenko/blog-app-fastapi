from typing import List

from pydantic import BaseModel


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
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(ShowUserInBlog):
    blogs: List[Blog] = []


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUserInBlog | None = None

    class Config:
        orm_mode = True
