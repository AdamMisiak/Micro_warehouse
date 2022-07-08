# pylint: disable=C0103
# invalid-name
from typing import List

from app2.database import get_db
from app2.domain import models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/batches",
    tags=["batches"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Batch, tags=["batches"])
def create_batch(batch: schemas.BatchCreate, db: Session = Depends(get_db)):
    # TODO can be moved to services or crud file
    db_batch = models.Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


@router.put("/{batch_id}", tags=["batches"])
def update_batch(batch_id: int, batch: schemas.Batch, db: Session = Depends(get_db)):
    db_batch = db.query(models.Batch).filter(models.Batch.id == batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    db_batch.update(
        {"id": batch.id, "sku": batch.sku, "reference": batch.reference, "quantity": batch.quantity, "eta": batch.eta}
    )
    db.commit()
    # TODO make response model Batch + what about relations
    return "batch updated"


@router.get("/{batch_id}", response_model=schemas.Batch, tags=["batches"])
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch


@router.get("/", response_model=List[schemas.Batch], tags=["batches"])
def read_all_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batches = db.query(models.Batch).offset(skip).limit(limit).all()
    return batches
