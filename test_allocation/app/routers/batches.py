from typing import List

from app import crud
from app.database import SessionLocal
from app.domain import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/batches",
    tags=["batches"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Batch, tags=["batches"])
def create_batch(batch: schemas.Batch, db: Session = Depends(get_db)):
    db_batch = crud.get_batch(db, batch_id=batch.id)
    if db_batch:
        raise HTTPException(status_code=400, detail="Batch already exists")
    return crud.create_batch(db=db, batch=batch)


@router.get("/", response_model=List[schemas.Batch], tags=["batches"])
def read_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batches = crud.get_batches(db, skip=skip, limit=limit)
    return batches


@router.get("/{batch_id}", response_model=schemas.Batch, tags=["batches"])
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = crud.get_batch(db, batch_id=batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch
