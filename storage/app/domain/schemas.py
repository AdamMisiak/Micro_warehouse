from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Batches
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


# Orders
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


# Utils
class Queue(BaseModel):
    url: str

    class Config:
        orm_mode = True


class QueueCreate(BaseModel):
    name: str
    delay: int = 0
    visibility: int = 60

    class Config:
        orm_mode = True


class Message(BaseModel):
    id: str
    body: str
    attributes: Optional[dict] = None

    class Config:
        orm_mode = True
