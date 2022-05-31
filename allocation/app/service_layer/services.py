from app.adapters import orm, repository
from app.domain import models
from app.service_layer import unit_of_work
from sqlalchemy.orm import Session


def get_batch(batch_id: int, uow: unit_of_work.AbstractUnitOfWork):
    # maybe skip uow?
    with uow:
        batch = uow.batches.get(batch_id=batch_id)
    return batch


# def get_batch(db: Session, batch_id: int):
#     return db.query(orm.Batch).filter(orm.Batch.id == batch_id).first()


# just for tests
def get_batches(limit: int, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        batches = uow.batches.get_all(limit=limit)
    return batches


# def get_batches(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(orm.Batch).offset(skip).limit(limit).all()


# def create_batch(db: Session, batch: models.Batch):
#     db_batch = orm.Batch(**batch.dict())
#     db.add(db_batch)
#     db.commit()
#     db.refresh(db_batch)
#     return db_batch


def create_batch(batch: models.Batch, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=batch.sku)
        if product is None:
            print("PRODUCT IS NONE - CREATING NEW")
            product = models.Product(id=10, sku=batch.sku, batches=[])
            uow.products.add(product)
        print(product)
        print(product.batches)
        print(batch.dict())
        product.batches.append(orm.Batch(**batch.dict()))
        print(product.batches)
        uow.commit()


def create_order_line(db: Session, order_line: models.OrderLine):
    db_order_line = orm.OrderLine(**order_line.dict())
    db.add(db_order_line)
    db.commit()
    db.refresh(db_order_line)
    return db_order_line


# just for tests


def get_product(sku: str, repository: repository.AbstractRepository):
    return repository.get(sku=sku)
