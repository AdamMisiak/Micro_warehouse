# pylint: disable=too-few-public-methods
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud
from .database import SessionLocal, engine
from .domain import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/batches/", response_model=schemas.Batch)
def create_batch(batch: schemas.Batch, db: Session = Depends(get_db)):
    db_batch = crud.get_batch(db, batch_id=batch.id)
    if db_batch:
        raise HTTPException(status_code=400, detail="Batch already exists")
    return crud.create_batch(db=db, batch=batch)


@app.get("/batches/", response_model=List[schemas.Batch])
def read_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batches = crud.get_batches(db, skip=skip, limit=limit)
    return batches


@app.get("/batches/{batch_id}", response_model=schemas.Batch)
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = crud.get_batch(db, batch_id=batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch
