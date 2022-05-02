from dataclasses import dataclass
from datetime import date
from typing import Optional, Set


@dataclass(unsafe_hash=True)
class OrderLine:
    '''
    OrderLine object is the part of bigger Order. 
    Immutable dataclass with no behaviour. 
    OrderLine is 'value equal' = two lines with the same values are equal.
    :order_id: id of the order
    :sku: stock-keeping unit = identification of product
    :qty: quantity of products
    '''
    order_id: str
    sku: str
    qty: int


class Batch:
    '''
    Batch object is the batch of stock ordered by purchasing department. 
    :ref: unique ID
    :sku: stock-keeping unit = identification of product
    :qty: quantity of products
    :eta: expected time of arrival
    '''
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta