# pylint: disable=too-few-public-methods
from app.adapters.orm import Base, engine
from app.routers import batches, order_lines, products
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(products.router)
app.include_router(batches.router)
app.include_router(order_lines.router)
