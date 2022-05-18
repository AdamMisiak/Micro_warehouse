# pylint: disable=too-few-public-methods
from datetime import date
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Batch(BaseModel):
    reference: str
    sku: str
    quantity: int
    eta: Optional[date]

    class Config:
        orm_mode = True


app = FastAPI()


@app.post("/items/")
async def create_item(item: Batch):
    return item
