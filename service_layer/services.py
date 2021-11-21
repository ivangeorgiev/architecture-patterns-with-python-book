import datetime
from typing import Optional
from domain import model
from adapters.repository import AbstractRepository

class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(orderid, sku, qty, repo:AbstractRepository, session) -> str:
    line = model.OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}.')
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def add_batch(ref:str, sku:str, qty:int, eta:Optional[datetime.date], repo:AbstractRepository, session):
    batch = model.Batch(ref, sku, qty, eta)
    repo.add(batch)
    session.commit()
