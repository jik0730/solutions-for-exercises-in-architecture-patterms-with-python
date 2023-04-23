from __future__ import annotations
from typing import Optional
from datetime import date

import model
from model import OrderLine, Batch
from repository import AbstractRepository

class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    line = OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref

def deallocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session):
    batches = repo.list()
    line = OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    for batch in batches:
        batch.deallocate(line)
    session.commit()

def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session):
    batch = Batch(ref, sku, qty, eta)
    repo.add(batch)
    session.commit()

