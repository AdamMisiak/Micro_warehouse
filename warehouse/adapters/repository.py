import abc
from typing import Set
from warehouse.domain import model


class AbstractRepository(abc.ABC):
    '''
    AbstractRepository is the port in port-adapter terminology. 
    Port is the interface between application and what we want to abstract away. 
    :seen: set of products
    '''
    def __init__(self):
        self.seen = set()  # type: Set[model.Product]

    def add(self, product: model.Batch):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Batch:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    '''
    SqlAlchemyRepository is the adapter in port-adapter terminology. 
    Adapter is the implementation behind interface or abstraction (port). 
    :session: 
    '''
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku):
        return self.session.query(model.Batch).filter_by(sku=sku).first()
