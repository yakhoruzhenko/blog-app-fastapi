from fastapi import FastAPI

from app.blog.controllers import admin, authentication, blogs, comments, users
from app.blog.database import Base, engine

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(comments.router)
