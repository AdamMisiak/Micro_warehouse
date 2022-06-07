# pylint: disable=too-few-public-methods, fixme, no-self-use, no-member, raise-missing-from
from datetime import date
from typing import List, Optional

from app.utils import exceptions
from pydantic import BaseModel


class OrderLine(BaseModel):
    # TODO: adding those should be another service - "ordering"?
    id: int
    sku: str
    quantity: int

    class Config:
        orm_mode = True


class Batch(BaseModel):
    # id: int
    sku: str
    reference: str
    quantity: int
    eta: Optional[date]
    _allocations: Optional[set]

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    class Config:
        orm_mode = True


class Product(BaseModel):
    sku: str
    version_number: Optional[int]
    batches: List[Batch]

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = self.batches[0]
            # batch = next(batch for batch in sorted(self.batches) if batch.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            raise exceptions.OutOfStock(f"Out of stock for sku {line.sku}")

    class Config:
        orm_mode = True
