from typing import List

from app.adapters.orm import get_db
from app.domain import models
from app.service_layer import services
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/batches",
    tags=["batches"],
    responses={404: {"description": "Not found"}},
)


# @router.post("/", response_model=models.Batch, tags=["batches"])
# def create_batch(batch: models.Batch, db: Session = Depends(get_db)):
#     db_batch = services.get_batch(db, batch_id=batch.id)
#     if db_batch:
#         raise HTTPException(status_code=400, detail="Batch already exists")
#     return services.create_batch(db=db, batch=batch)


@router.post("/", response_model=models.Batch, tags=["batches"])
def create_batch(batch: models.BatchCreate, db: Session = Depends(get_db)):
    return services.create_batch(db, batch=batch)


@router.get("/{batch_id}", response_model=models.Batch, tags=["batches"])
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = services.get_batch(db, batch_id=batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch


@router.get("/", response_model=List[models.Batch], tags=["batches"])
def read_all_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batches = services.get_all_batches(db, skip=skip, limit=limit)
    return batches


# @router.get("/", response_model=List[models.Batch], tags=["batches"])
# def read_batches(limit: int = 100, db: Session = Depends(get_db)):
#     batches = services.get_batches(limit=limit, uow=unit_of_work.SqlAlchemyUnitOfWork(session=db))
#     return batches


# @router.get("/{batch_id}", response_model=models.Batch, tags=["batches"])
# def read_batch(batch_id: int, db: Session = Depends(get_db)):
# db_batch = services.get_batch(db, batch_id=batch_id)

# db_batch = services.get_batch(batch_id=batch_id, uow=unit_of_work.SqlAlchemyUnitOfWork(session=db))
# if db_batch is None:
#     raise HTTPException(status_code=404, detail="Batch not found")
# return db_batch

# db_batch = services.get_batch(db, batch_id=batch_id)
# if db_batch is None:
#     raise HTTPException(status_code=404, detail="Batch not found")
# return db_batch
