from app.adapters import orm
from app.domain import models
from sqlalchemy.orm import Session


def get_batch(db: Session, batch_id: int):
    return db.query(orm.Batch).filter(orm.Batch.id == batch_id).first()


def get_batches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(orm.Batch).offset(skip).limit(limit).all()


def create_batch(db: Session, batch: models.Batch):
    db_batch = orm.Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch
