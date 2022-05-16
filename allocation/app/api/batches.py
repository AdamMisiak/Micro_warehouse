from typing import List

from app.adapters import repository
from app.api import db_manager
from app.domain.models import Batch
from fastapi import APIRouter

batches = APIRouter()


@batches.post("/", status_code=201)
async def create(payload: Batch):
    await db_manager.add_batch(payload)
    return payload


@batches.get("/", response_model=List[Batch])
async def get():
    results = repository.SqlAlchemyRepository()
    # print(batches.get_all())
    return await results.get_all()
    # return await db_manager.get_all_batches()
