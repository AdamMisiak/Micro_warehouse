from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BatchBase(BaseModel):
    sku: str
    reference: str
    quantity: int
    eta: Optional[datetime]


class BatchCreate(BatchBase):
    pass


class Batch(BatchBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: Optional[int]
    sku: str
    quantity: int

    class Config:
        orm_mode = True


class OrderWithBatch(Order):
    batch: Optional[Batch] = None
