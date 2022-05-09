from app.api.models import Batch
from app.api.db import batches, database


async def add_batch(payload: Batch):
    query = batches.insert().values(**payload.dict())
    await database.connect()
    return await database.execute(query=query)

async def get_all_batches():
    query = batches.select()
    await database.connect()
    return await database.fetch_all(query=query)
