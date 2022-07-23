# pylint: disable=C0103
# invalid-name
from typing import List

from app.database import get_db
from app.domain import models, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/batches",
    tags=["Batches"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Batch, tags=["Batches"])
def create_batch(batch: schemas.BatchCreate, db: Session = Depends(get_db)):
    # TODO can be moved to services or crud file
    db_batch = models.Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    # TODO add publish event after each commit
    db.refresh(db_batch)
    return db_batch


@router.put("/{batch_id}", tags=["Batches"])
def update_batch(batch_id: int, batch: schemas.BatchCreate, db: Session = Depends(get_db)):
    db_batch = db.query(models.Batch).filter(models.Batch.id == batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    db_batch.update(
        {"id": batch_id, "sku": batch.sku, "reference": batch.reference, "quantity": batch.quantity, "eta": batch.eta}
    )
    db.commit()
    return {"status_code": 200, "message": f"Batch id: {batch_id} has been updated"}


@router.get("/{batch_id}", response_model=schemas.Batch, tags=["Batches"])
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch


@router.get("/", response_model=List[schemas.Batch], tags=["Batches"])
def read_all_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batches = db.query(models.Batch).offset(skip).limit(limit).all()
    return batches
