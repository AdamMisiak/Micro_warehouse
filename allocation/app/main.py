# pylint: disable=too-few-public-methods
# from app.adapters.orm import Base, engine
from app.adapters.orm import create_db_and_tables, engine
from app.routers import batches, order_lines, products
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Base.metadata.create_all(bind=engine)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(products.router)
app.include_router(batches.router)
app.include_router(order_lines.router)
