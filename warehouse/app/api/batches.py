from fastapi import Header, APIRouter
from app.api.models import Batch
from app.api import db_manager

batches_router = APIRouter()


@batches_router.post('/', status_code=201)
async def add_batch(payload: Batch):
    await db_manager.add_batch(payload)
    return payload
