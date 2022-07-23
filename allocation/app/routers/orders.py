# pylint: disable=C0103
# invalid-name
from typing import List

import localstack_client.session as boto3
from app.database import get_db
from app.domain import models, schemas
from app.utils import exceptions, settings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # TODO can be moved to services or crud file
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[schemas.OrderWithBatch], tags=["Orders"])
def read_all_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=schemas.OrderWithBatch, tags=["Orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/{order_id}/allocate", response_model=schemas.Batch, tags=["Orders"])
def allocate_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise exceptions.OrderNotFound("Order not found")
    if order.is_allocated():
        raise exceptions.OrderAlreadyAllocated("Order is already allocated")
    batch = db.query(models.Batch).order_by(models.Batch.quantity).filter(models.Batch.sku == order.sku).first()
    if not batch:
        raise exceptions.InvalidSku(f"Invalid sku {order.sku}")
    batch.allocate(order)
    # db.add(batch)
    # db.commit()
    # db.refresh(batch)

    return batch


@router.get("/{order_id}/messages")
def read_messages(order_id: int, db: Session = Depends(get_db)):
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
    messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
    for message in messages:
        print(f"Received message: {message.message_id}, {message.body}, {message.message_attributes}")
        # message.delete()
        # print(message.delete())
    return "test"
