import datetime
from typing import Optional
from ..domain import model
from ..adapters.repository import AbstractRepository
from ..service_layer.unit_of_work import AbstractUnitOfWork

class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(orderid, sku, qty, uow) -> str:
    line = model.OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku {line.sku}.')
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref


def add_batch(ref:str, sku:str, qty:int, eta:Optional[datetime.date], uow:AbstractUnitOfWork):
    batch = model.Batch(ref, sku, qty, eta)
    with uow:
        uow.batches.add(batch)
        uow.commit()
