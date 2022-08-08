from app.domain.models import Base
from app.routers import orders, utils
from fastapi import FastAPI

from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(orders.router)
app.include_router(utils.router)
