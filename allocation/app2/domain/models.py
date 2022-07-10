from app2.database import Base
from app2.utils import exceptions
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    sku = Column(String, default=None)
    quantity = Column(Integer, default=10)
    batch_id = Column(Integer, ForeignKey("batch.id"))
    batch = relationship("Batch", back_populates="order")

    def is_allocated(self) -> bool:
        return self.batch is not None


class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True, index=True, nullable=True, default=None)
    sku = Column(String, default=None)
    reference = Column(String, default=None)
    quantity = Column(Integer, default=10)
    eta = Column(DateTime, nullable=True)
    order = relationship("Order", back_populates="batch")

    def can_allocate(self, line: Order) -> bool:
        return self.sku == line.sku and int(self.quantity) >= int(line.quantity)

    def allocate(self, line: Order):
        if self.can_allocate(line):
            self.quantity = int(self.quantity)
            self.quantity -= line.quantity
            line.batch = self
        else:
            raise exceptions.OutOfStock(f"Out of stock {self.sku}")
