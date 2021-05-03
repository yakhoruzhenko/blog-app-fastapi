from fastapi import FastAPI
from blog import models, database
from blog.routers import blog, user, authentication

models.Base.metadata.create_all(database.engine)
app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
