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
    secret: str | None = None


class ShowUserInBlog(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class Comment(BaseModel):
    blog_title: str
    text: str


class ShowComment(BaseModel):
    id: int
    blog_title: str
    user_name: str
    text: str

    class Config:
        orm_mode = True


class ShowUser(ShowUserInBlog):
    blogs: List[Blog] = []
    comments: List[ShowComment] = []


class ShowBlog(BaseBlog):
    creator: ShowUserInBlog
    comments: List[ShowComment] = []

    class Config:
        orm_mode = True
