from typing import List

from model import OrderLine, Batch


def allocate(line: OrderLine, batches: List[Batch]):
    batch = sorted(batches)[0]
    batch.allocate(line)
