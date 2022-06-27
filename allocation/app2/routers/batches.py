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
    db_batch = models.Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


# @router.get("/{batch_id}", response_model=models.Batch, tags=["batches"])
# def read_batch(batch_id: int, db: Session = Depends(get_db)):
#     db_batch = services.get_batch(db, batch_id=batch_id)
#     if db_batch is None:
#         raise HTTPException(status_code=404, detail="Batch not found")
#     return db_batch


# @router.get("/", response_model=List[models.Batch], tags=["batches"])
# def read_all_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     batches = services.get_all_batches(db, skip=skip, limit=limit)
#     return batches
