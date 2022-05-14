# import abc

# from app.api import models

# class AbstractRepository(abc.ABC):
#     '''
#     AbstractRepository is the port in port-adapter terminology.
#     Port is the interface between application and what we want to abstract away.
#     :seen: set of products
#     '''
#     def __init__(self):
#         self.seen = set()

#     def add(self, product: models.Batch):
#         self._add(product)
#         self.seen.add(product)

#     def get(self, sku) -> models.Batch:
#         product = self._get(sku)
#         if product:
#             self.seen.add(product)
#         return product

#     @abc.abstractmethod
#     def _add(self, product: models.Batch):
#         raise NotImplementedError

#     @abc.abstractmethod
#     def _get(self, sku) -> models.Batch:
#         raise NotImplementedError


# class SqlAlchemyRepository(AbstractRepository):
#     '''
#     SqlAlchemyRepository is the adapter in port-adapter terminology.
#     Adapter is the implementation behind interface or abstraction (port).
#     :session:
#     '''
#     def __init__(self, session):
#         super().__init__()
#         self.session = session

#     def _add(self, product):
#         self.session.add(product)

#     def _get(self, sku):
#         return self.session.query(models.Batch).filter_by(sku=sku).first()
