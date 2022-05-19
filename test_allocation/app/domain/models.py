# pylint: disable=too-few-public-methods, relative-beyond-top-level
from app.database import Base
from sqlalchemy import Column, Date, Integer, String


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, index=True)
    sku = Column(String, index=True)
    quantity = Column(Integer)
    eta = Column(Date)
