# pylint: disable=too-few-public-methods, fixme, no-self-use
from datetime import date
from typing import List, Optional

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

    # def allocate(self, line) -> str:
    # def allocate(self):
    #     print("allocating")

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

    # def allocate(self, line) -> str:
    def allocate(self):
        print("allocating")

    class Config:
        orm_mode = True
