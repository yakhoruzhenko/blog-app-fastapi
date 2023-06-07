from fastapi import FastAPI

from app.blog.database import Base, engine
from app.blog.routers import admin, authentication, blog, user

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(blog.router)
