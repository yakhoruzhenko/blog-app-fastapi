from typing import List, Optional

from pydantic import BaseModel


class BaseBlog(BaseModel):
    title: str
    body: str


class Blog(BaseBlog):
    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str
    secret: Optional[str] = None


class ShowUserInBlog(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class Comment(BaseModel):
    blog_title: str
    text: str


class ShowComment(BaseModel):
    id: int
    blog_title: str
    user_name: str
    text: str

    class Config:
        from_attributes = True


class ShowUser(ShowUserInBlog):
    blogs: List[Blog] = []
    comments: List[ShowComment] = []


class ShowBlog(BaseBlog):
    id: int
    creator: ShowUserInBlog
    comments: List[ShowComment] = []

    class Config:
        from_attributes = True
