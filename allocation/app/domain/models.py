# pylint: disable=too-few-public-methods, fixme, no-self-use
from datetime import date
from typing import List, Optional

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


class Product(BaseModel):
    id: int
    sku: str
    version_number: int
    batches: List[Batch]

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
