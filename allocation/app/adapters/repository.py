import abc
from typing import Set

from allocation.app.domain import models


class AbstractRepository(abc.ABC):
    def __init__(self):
        # need to understand the idea of seen
        self.seen = set()  # type: Set[models.Product]

    def add(self, batch: models.Batch):
        self._add(batch)
        self.seen.add(batch)

    def get(self, sku) -> models.Batch:
        batch = self._get(sku)
        if batch:
            self.seen.add(batch)
        return batch

    @abc.abstractmethod
    def _add(self, batch: models.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> models.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, batch):
        pass
        # db.add(db_batch)

    def _get(self, sku):
        pass
        # return db.query(orm.Batch).offset(skip).limit(limit).all()
