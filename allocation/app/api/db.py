from sqlalchemy import (Column, Integer, MetaData, String, Table, Date,
                        create_engine)

from databases import Database

DATABASE_URL = 'postgresql://admin:admin@allocation_db/allocation_db'

engine = create_engine(DATABASE_URL)
metadata = MetaData()


order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255)),
)


batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

database = Database(DATABASE_URL)