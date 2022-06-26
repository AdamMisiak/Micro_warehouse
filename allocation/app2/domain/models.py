from app2.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True, nullable=True, default=None)
    sku = Column(String, default=True)
    reference = Column(String, default=True)
    quantity = Column(String, default=True)
    eta = Column(DateTime, nullable=True)
