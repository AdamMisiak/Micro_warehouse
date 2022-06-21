from app.domain import models
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

# def create_batch(batch: models.BatchBase, uow: unit_of_work.AbstractUnitOfWork):
#     with uow:
#         product = uow.products.get(sku=batch.sku)
#         if product is None:
#             product = models.ProductWithBatches(sku=batch.sku, batches=[])
#             uow.products.add(product)
#         product.batches.append(models.Batch(**batch.dict()))
#         print(product)
#         print(product.batches)
#         uow.commit()
#     print(product)
#     print(product.batches)
#     return batch


# Batches - with repo
# def create_batch(batch: models.Batch, repository: repository.AbstractRepository):
#     batch = repository.add(batch, models.Batch)
#     print(batch)
#     print('--'*50)
#     product = repository.get(sku=batch.sku)
#     print(product)
#     print('--'*50)
#     product.batches.append(batch)
#     repository.session.commit()
#     # product.batches.append(repository.add(batch, models.Batch))
#     return batch


def create_batch(db: Session, batch: models.Batch):
    db_batch = models.Batch.from_orm(batch)
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


def get_batch(db: Session, batch_id: int):
    return db.query(models.Batch).filter(models.Batch.id == batch_id).first()


def get_all_batches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Batch).offset(skip).limit(limit).all()


# only used in allocation
def get_batches_by_sku(db: Session, sku: str):
    return db.query(models.Batch).filter(models.Batch.sku == sku).all()


# # Products
# def get_product(sku: str, repository: repository.AbstractRepository):
#     return repository.get(sku=sku)

# def get_all_products(limit: int, repository: repository.AbstractRepository):
#     return repository.get_all(limit=limit)


# Order lines
def create_order_line(db: Session, order_line: models.OrderLine):
    db_order_line = models.OrderLine.from_orm(order_line)
    db.add(db_order_line)
    db.commit()
    db.refresh(db_order_line)
    return db_order_line


def get_order_line(db: Session, order_line_id: int):
    return db.query(models.OrderLine).filter(models.OrderLine.id == order_line_id).first()


def allocate(
    db: Session,
    order_line: models.OrderLine,
    # id: str, sku: str, quantity: int,
    # uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    batches = get_batches_by_sku(db, sku=order_line.sku)
    print(batches)
    if not batches:
        raise exceptions.InvalidSku(f"Invalid sku {order_line.sku}")
    print("allocate here!")
    # batch_reference = product.allocate(line)
    # uow.commit()
    return "allocate"
