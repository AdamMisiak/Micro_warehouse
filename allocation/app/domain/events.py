from dataclasses import dataclass


class Event:
    pass


@dataclass
class OutOfStock(Event):
    event_type: str
    sku: str
