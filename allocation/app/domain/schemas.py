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


class OrderBase(BaseModel):
    sku: str
    quantity: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class OrderWithBatch(Order):
    batch: Optional[Batch] = None


class Queue(BaseModel):
    name: str

    class Config:
        orm_mode = True
