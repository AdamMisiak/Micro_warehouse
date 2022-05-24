# pylint: disable=too-few-public-methods, fixme, no-self-use
from datetime import date
from typing import Optional

from pydantic import BaseModel


class Batch(BaseModel):
    id: int
    reference: str
    sku: str
    quantity: int
    eta: Optional[date]

    # def allocate(self, line) -> str:
    def allocate(self):
        print("allocating")

    class Config:
        orm_mode = True


class OrderLine(BaseModel):
    # TODO: adding those should be another service - "ordering"?
    id: int
    sku: str
    quantity: int

    class Config:
        orm_mode = True
