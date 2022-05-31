# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

import abc

from app.adapters import repository

# from sqlalchemy.orm.session import Session


class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        pass
        # self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    # @abc.abstractmethod
    # def rollback(self):
    #     raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        self.products = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        # self.session.expunge_all()
        # print("CLOSE")
        self.session.close()

    def _commit(self):
        # print("COMMIT")
        self.session.commit()

    # def rollback(self):
    #     self.session.rollback()
