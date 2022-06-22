# pylint: disable=too-few-public-methods, fixme, no-self-use, no-member, raise-missing-from
from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class OrderLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    sku: str
    quantity: int


class Product(SQLModel, table=True):
    sku: str = Field(default=None, primary_key=True)
    version_number: Optional[int] = Field(default="0")
    batches: List["Batch"] = Relationship(back_populates="product", sa_relationship_kwargs={"lazy": "joined"})


class BatchBase(SQLModel):
    sku: str = Field(default=None, foreign_key="product.sku")
    reference: str
    quantity: int
    eta: Optional[date]


class Batch(BatchBase, table=True):
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    product: Optional[Product] = Relationship(back_populates="batches")
    # _allocations: PrivateAttr(default=set()) #Set[OrderLine]

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self.quantity -= line.quantity
        else:
            print("no enough quantity")

    # def deallocate(self, line: OrderLine):
    #     if line in self._allocations:
    #         self._allocations.remove(line)

    # @property
    # def allocated_quantity(self) -> int:
    #     return sum(line.quantity for line in self._allocations)

    # @property
    # def available_quantity(self) -> int:
    #     return self.quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.quantity >= line.quantity


class BatchCreate(BatchBase):
    pass


class ProductWithBatches(Product):
    batches: List[BatchBase] = []
