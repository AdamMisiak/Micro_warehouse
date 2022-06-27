from typing import List

from app2.database import get_db
from app2.domain import models, schemas
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


# @router.get("/{batch_id}", response_model=schemas.Batch, tags=["orders"])
# def read_batch(batch_id: int, db: Session = Depends(get_db)):
#     db_batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
#     if db_batch is None:
#         raise HTTPException(status_code=404, detail="Batch not found")
#     return db_batch


# @router.get("/", response_model=List[schemas.Batch], tags=["orders"])
# def read_all_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     batches = db.query(models.Batch).offset(skip).limit(limit).all()
#     return batches
