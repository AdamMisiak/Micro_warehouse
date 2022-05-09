from sqlalchemy import (Column, Integer, MetaData, String, Table, Date,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URL = 'postgresql://admin:admin@allocation_db/allocation_db'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

batches = Table(
    'batches',
    metadata,
    Column('ref', String(50), primary_key=True),
    Column('sku', String(50)),
    Column('qty', String(250)),
    Column('eta', Date),

)

database = Database(DATABASE_URL)