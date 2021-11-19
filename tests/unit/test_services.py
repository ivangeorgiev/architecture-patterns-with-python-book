from domain import model
from adapters import repository
from service_layer import services

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

def test_allocate_commits():
    line = model.OrderLine("o1", "BLACK-LIGHT", 10)
    batch = model.Batch("b1", "BLACK-LIGHT", 100, eta=None)
    repo = repository.FakeRepository([batch])
    session = FakeSession()
    services.allocate(line, repo, session)

    assert session.committed is True

def test_returns_allocation():
    line = model.OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = repository.FakeRepository([batch])
    result = services.allocate(line, repo, FakeSession())

    assert result == "b1"
