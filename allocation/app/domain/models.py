# pylint: disable=too-few-public-methods
from datetime import date
from typing import Optional

from pydantic import BaseModel


class Batch(BaseModel):
    reference: str
    sku: str
    quantity: int
    eta: Optional[date]


class OrderLine(BaseModel):
    order_id: str
    sku: str
    quantity: int
