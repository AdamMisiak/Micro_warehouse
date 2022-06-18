# pylint: disable=too-few-public-methods
# from app.adapters.orm import Base, engine
from app.adapters.orm import engine
from app.routers import batches, order_lines, products
from fastapi import FastAPI
from sqlmodel import SQLModel

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(batches.router)
app.include_router(order_lines.router)
