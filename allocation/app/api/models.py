from pydantic import BaseModel
from typing import Optional
from datetime import date


class Batch(BaseModel):
    ref: str
    sku: str
    qty: str
    eta: Optional[date]

class OrderLine(BaseModel):
    order_id: str
    sku: str
    qty: int