# pylint: disable=redefined-outer-name
import abc
from typing import List

from app.api.db import batches, database
from app.domain import models


class AbstractRepository(abc.ABC):
    """
    AbstractRepository is the port in port-adapter terminology.
    Port is the interface between application and what we want to abstract away.
    :seen: set of batches
    """

    def __init__(self):
        self.seen = set()

    def add(self, batch: models.Batch):
        self._add(batch)
        # self.seen.add(batch)

    def get(self, sku) -> models.Batch:
        batch = self._get(sku)
        if batch:
            self.seen.add(batch)
        return batch

    def get_all(self) -> List[models.Batch]:
        return self._get_all()

    @abc.abstractmethod
    def _add(self, batch: models.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> models.Batch:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_all(self) -> models.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """
    SqlAlchemyRepository is the adapter in port-adapter terminology.
    Adapter is the implementation behind interface or abstraction (port).
    :session:
    """

    def __init__(self, session=database):
        super().__init__()
        self.session = session

    def _add(self, batch):
        self.session.add(batch)

    def _get(self, sku):
        return self.session.query(models.Batch).filter_by(sku=sku).first()

    async def _get_all(self):
        # find solution for this session connect
        await self.session.connect()
        return await self.session.fetch_all(query=batches.select())
