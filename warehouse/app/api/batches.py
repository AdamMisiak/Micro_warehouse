from typing import List
from fastapi import Header, APIRouter
from app.api.db import database, batches
from app.api.models import Batch
# from app.api import db_manager

batches = APIRouter()

# @batches.get('/', response_model=List[MovieOut])
# async def index():
#     return await db_manager.get_all_movies()

@batches.post('/', status_code=201)
async def add_batch(payload: Batch):
    batch_ref = await database.execute(query=batches.insert().values(**payload.dict()))
    print(batch_ref)
    response = {
        'ref': batch_ref,
        **payload.dict()
    }

    return response