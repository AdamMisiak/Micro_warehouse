import abc
from typing import Set

from app.adapters import orm
from app.domain import models


class AbstractRepository(abc.ABC):
    def __init__(self):
        # need to understand the idea of seen
        self.seen = set()  # type: Set[models.Product]

    def add(self, batch: models.Batch):
        self._add(batch)
        self.seen.add(batch)

    def get(self, batch_id) -> models.Batch:
        batch = self._get(batch_id)
        if batch:
            self.seen.add(batch)
        return batch

    def get_all(self, limit) -> models.Batch:
        batches = self._get_all(limit=limit)
        return batches

    @abc.abstractmethod
    def _add(self, batch: models.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, batch_id) -> models.Batch:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(self, limit) -> models.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, batch):
        pass
        # db.add(db_batch)

    def _get(self, batch_id):
        return self.session.query(orm.Batch).filter(orm.Batch.id == batch_id).first()
        # return db.query(orm.Batch).offset(skip).limit(limit).all()

    def _get_all(self, limit):
        return self.session.query(orm.Batch).limit(limit).all()
