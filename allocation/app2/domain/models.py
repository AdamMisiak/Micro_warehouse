from app2.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True, nullable=True, default=None)
    sku = Column(String, default=None)
    reference = Column(String, default=None)
    quantity = Column(Integer, default=10)
    eta = Column(DateTime, nullable=True)
