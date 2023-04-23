from datetime import date
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    ref: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.ref = ref
        self.sku = sku
        self.available_quantity = qty
        self.eta = eta

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty
    
    def can_allocate(self, line: OrderLine) -> bool:
        return line.sku == self.sku and self.available_quantity >= line.qty
    
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


