from typing import List

from app.api import db_manager
from app.domain.models import OrderLine
from fastapi import APIRouter

order_lines = APIRouter()


@order_lines.post("/", status_code=201)
async def create(payload: OrderLine):
    await db_manager.add_order_line(payload)
    return payload


@order_lines.get("/", response_model=List[OrderLine])
async def get():
    return await db_manager.get_all_order_lines()
