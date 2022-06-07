from app.adapters import orm
from app.domain import models
from app.service_layer import unit_of_work
from app.utils import exceptions
from sqlalchemy.orm import Session

# def get_batch(batch_id: int, uow: unit_of_work.AbstractUnitOfWork):
#     with uow:
#         batch = uow.batches.get(batch_id=batch_id)
#     return batch


# def get_batch(db: Session, batch_id: int):
#     return db.query(orm.Batch).filter(orm.Batch.id == batch_id).first()


# # just for tests
# def get_batches(limit: int, uow: unit_of_work.AbstractUnitOfWork):
#     with uow:
#         batches = uow.batches.get_all(limit=limit)
#     return batches


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
            product = models.Product(sku=batch.sku, batches=[])
            uow.products.add(product)
        product.batches.append(orm.Batch(**batch.dict()))
        uow.commit()
    return batch


def create_order_line(db: Session, order_line: models.OrderLine):
    db_order_line = orm.OrderLine(**order_line.dict())
    db.add(db_order_line)
    db.commit()
    db.refresh(db_order_line)
    return db_order_line


# just for tests
def get_product(sku: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        return uow.products.get(sku=sku)


# just for tests
def get_all_products(limit: int, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        return uow.products.get_all(limit=limit)


def allocate(
    order_line: models.OrderLine,
    # id: str, sku: str, quantity: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = order_line
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise exceptions.InvalidSku(f"Invalid sku {line.sku}")
        print(product)
        print(dir(product))
        print(models.Product(sku=product.sku, version_number=product.version_number, batches=product.batches))
        # maybe add this: https://github.com/tiangolo/sqlmodel
        # or this: https://github.com/tiangolo/pydantic-sqlalchemy
        batch_reference = product.allocate(line)
        uow.commit()
    return batch_reference
