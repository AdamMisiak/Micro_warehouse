# pylint: disable=C0103
# invalid-name
from typing import List

from app2.database import get_db
from app2.domain import models, schemas
from app2.utils import exceptions
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Order, tags=["orders"])
def create_order(order: schemas.Order, db: Session = Depends(get_db)):
    # TODO can be moved to services or crud file
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=schemas.Order, tags=["orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/{order_id}/allocate", response_model=schemas.Batch, tags=["orders"])
def allocate_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    batch = db.query(models.Batch).order_by(models.Batch.quantity).filter(models.Batch.sku == order.sku).first()
    if not batch:
        raise exceptions.InvalidSku(f"Invalid sku {order.sku}")
    batch.allocate(order)
    db.add(batch)
    db.commit()
    db.refresh(batch)

    return batch


@router.get("/", response_model=List[schemas.OrderWithBatch], tags=["orders"])
def read_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders
