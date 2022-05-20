# pylint: disable=too-few-public-methods
from app.routers import batches
from fastapi import FastAPI

from .database import engine
from .domain import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(batches.router)
