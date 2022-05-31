import abc
from typing import Set

from app.adapters import orm
from app.domain import models


class AbstractRepository(abc.ABC):
    def __init__(self):
        # need to understand the idea of seen
        self.seen = set()  # type: Set[models.Batch]

    def add(self, product: models.Product):
        # self.seen.add(product)
        db_product = self._add(product)
        return db_product

    def get(self, sku) -> models.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_all(self, limit) -> models.Product:
        products = self._get_all(limit=limit)
        return products

    @abc.abstractmethod
    def _add(self, product: models.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> models.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(self, limit) -> models.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        # changing from pydantic schema to ORM model
        db_product = orm.Batch(**product.dict())
        self.session.add(db_product)
        # self.session.commit()
        # self.session.refresh(db_product)
        return db_product

    def _get(self, sku):
        return self.session.query(orm.Product).filter(orm.Product.sku == sku).first()

    def _get_all(self, limit):
        return self.session.query(orm.Product).limit(limit).all()
