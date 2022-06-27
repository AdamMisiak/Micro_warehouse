from app2.domain.models import Base
from app2.routers import batches
from fastapi import FastAPI

from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(batches.router)