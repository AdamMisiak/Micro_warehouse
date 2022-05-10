from pydantic import BaseModel
from typing import Optional
from datetime import date


class Batch(BaseModel):
    reference: str
    sku: str
    quantity: int
    eta: Optional[date]

class OrderLine(BaseModel):
    order_id: str
    sku: str
    quantity: int