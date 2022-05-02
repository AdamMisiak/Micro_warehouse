from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import date

from warehouse.domain import model

if TYPE_CHECKING:
    from . import unit_of_work


class InvalidSku(Exception):
    pass


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        # TODO check how to get batches for UOW
        uow.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()

# def list_batches(
#     ref: str, sku: str, qty: int, eta: Optional[date],
#     uow: unit_of_work.AbstractUnitOfWork,
# ):
#     with uow:
#         uow.batches.append(model.Batch(ref, sku, qty, eta))
#         uow.commit()

