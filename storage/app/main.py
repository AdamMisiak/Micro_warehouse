from app.domain.models import Base
from app.routers import batches
from fastapi import FastAPI

from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(batches.router)
