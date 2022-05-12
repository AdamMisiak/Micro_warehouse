from fastapi import Header, APIRouter
from app.api.models import OrderLine
from app.api import db_manager
from typing import List

order_lines = APIRouter()


@order_lines.post('/', status_code=201)
async def create(payload: OrderLine):
    await db_manager.add_order_line(payload)
    return payload

@order_lines.get('/', response_model=List[OrderLine])
async def get():
    return await db_manager.get_all_order_lines()
