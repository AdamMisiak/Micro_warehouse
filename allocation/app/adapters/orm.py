# pylint: disable=too-few-public-methods, relative-beyond-top-level
from sqlalchemy import Column, Date, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql://admin:admin@allocation_db/allocation_db"

engine = create_engine(DATABASE_URL)
# , expire_on_commit=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    sku = Column(String, primary_key=True, index=True)
    version_number = Column(Integer, nullable=False, default="0")
    batches = relationship("Batch", lazy="subquery", back_populates="product")


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(ForeignKey("products.sku"))
    reference = Column(String, index=True)
    quantity = Column(Integer)
    eta = Column(Date)
    product = relationship("Product", back_populates="batches")


class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    quantity = Column(Integer)


def get_db():
    # could be changed to async in the future - check docs
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
