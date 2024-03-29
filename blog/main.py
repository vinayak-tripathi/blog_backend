from fastapi import FastAPI

from . import models
from .router import blog, user, authentication
from .database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
