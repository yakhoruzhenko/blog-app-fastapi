from fastapi import FastAPI

from app.blog.database import Base, engine
from app.blog.routers import admin, authentication, blogs, comments, users

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(comments.router)
