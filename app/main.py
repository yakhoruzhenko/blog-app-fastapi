from fastapi import FastAPI

from app.blog.database import Base, engine
from app.blog.routers import authentication, blog, user

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
