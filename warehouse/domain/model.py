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
    :sku: stock-keeping unit = identyfication of product
    :qty: quantity of products
    '''
    order_id: str
    sku: str
    qty: int
