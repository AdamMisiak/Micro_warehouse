from pydantic import BaseModel
from typing import Optional
from datetime import date


class Batch(BaseModel):
    ref: str
    sku: str
    qty: str
    eta: Optional[date]
