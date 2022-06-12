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


class BatchCreate(BatchBase):
    pass


class ProductWithBatches(Product):
    batches: List[BatchBase] = []
