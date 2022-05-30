# pylint: disable=too-few-public-methods, relative-beyond-top-level
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://admin:admin@allocation_db/allocation_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, index=True)
    sku = Column(String, index=True)
    quantity = Column(Integer)
    eta = Column(Date)


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
