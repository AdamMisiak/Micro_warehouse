from app.api.db import batches, database, order_lines
from app.domain.models import Batch, OrderLine


async def add_batch(payload: Batch):
    query = batches.insert().values(**payload.dict())
    await database.connect()
    return await database.execute(query=query)


async def get_all_batches():
    query = batches.select()
    await database.connect()
    return await database.fetch_all(query=query)


async def add_order_line(payload: OrderLine):
    query = order_lines.insert().values(**payload.dict())
    await database.connect()
    return await database.execute(query=query)


async def get_all_order_lines():
    query = order_lines.select()
    await database.connect()
    return await database.fetch_all(query=query)
