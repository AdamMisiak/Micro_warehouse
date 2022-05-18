# pylint: disable=too-few-public-methods
from datetime import date
from typing import Optional

from pydantic import BaseModel


class Batch(BaseModel):
    id: int
    reference: str
    sku: str
    quantity: int
    eta: Optional[date]

    class Config:
        orm_mode = True
