# pylint: disable=too-few-public-methods
from app.adapters.orm import Base, engine
from app.routers import batches
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(batches.router)
