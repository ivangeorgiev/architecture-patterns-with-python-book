import pytest
from allocation.adapters import repository
from allocation.service_layer import services, unit_of_work

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = repository.FakeRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_allocate_commits():
    uow = FakeUnitOfWork()
    line = ("o1", "BLACK-LIGHT", 10)
    batch = ("b1", "BLACK-LIGHT", 100, None)
    services.add_batch(*batch, uow)
    services.allocate(*line, uow)

    assert uow.committed is True

def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    line = ("o1", "COMPLICATED-LAMP", 10)
    batch = ("b1", "COMPLICATED-LAMP", 100, None)
    services.add_batch(*batch, uow)

    result = services.allocate(*line, uow)

    assert result == "b1"

def test_add_batch_adds_a_batch_to_repository():
    uow = FakeUnitOfWork()
    batch = ('b1', 'BREAD-SWORD', 100, None)
    services.add_batch(*batch, uow)
    assert uow.committed is True
    assert uow.batches.get('b1') is not None

def test_allocate_errors_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, uow)

