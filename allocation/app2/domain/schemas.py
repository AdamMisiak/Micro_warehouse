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
