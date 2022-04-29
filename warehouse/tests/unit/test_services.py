from unittest import mock
import pytest
from warehouse.adapters import repository
from warehouse.service_layer import services, unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches):
        super().__init__()
        self.batches = set(batches)

    def _add(self, product):
        self.batches.add(product)

    def _get(self, sku):
        return next((p for p in self.batches if p.sku == sku), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_batch_for_new_product():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "BIG-TABLE", 100, None, uow)
    assert uow.batches.get("BIG-TABLE") is not None
    assert uow.committed
