from datetime import date, timedelta
import pytest

from model import Batch, OrderLine
from service import allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=today)
    line = OrderLine('order-ref', 'SMALL-TABLE', 2)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required():
    batch = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=today)
    line = OrderLine('order-ref', 'SMALL-TABLE', qty=10)
    assert batch.can_allocate(line) is True

def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch('batch-001', 'SMALL-TABLE', qty=5, eta=today)
    line = OrderLine('order-ref', 'SMALL-TABLE', qty=10)
    assert batch.can_allocate(line) is False

def test_can_allocate_if_available_equal_to_required():
    batch = Batch('batch-001', 'SMALL-TABLE', qty=10, eta=today)
    line = OrderLine('order-ref', 'SMALL-TABLE', qty=10)
    assert batch.can_allocate(line) is True

def test_prefers_warehouse_batches_to_shipments():
    batch_warehouse = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=None)
    batch_shipment = Batch('batch-002', 'SMALL-TABLE', qty=20, eta=today)
    line = OrderLine('order-ref', 'SMALL-TABLE', qty=10)
    allocate(line, [batch_warehouse, batch_shipment])
    assert batch_warehouse.available_quantity == 10
    assert batch_shipment.available_quantity == 20

def test_prefers_earlier_batches():
    batch_today = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=today)
    batch_tomorrow = Batch('batch-002', 'SMALL-TABLE', qty=20, eta=tomorrow)
    line = OrderLine('order-ref', 'SMALL-TABLE', qty=10)
    allocate(line, [batch_today, batch_tomorrow])
    assert batch_today.available_quantity == 10
    assert batch_tomorrow.available_quantity == 20

