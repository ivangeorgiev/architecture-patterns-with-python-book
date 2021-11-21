from adapters import repository
from service_layer import services

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

def test_allocate_commits():
    line = ("o1", "BLACK-LIGHT", 10)
    batch = ("b1", "BLACK-LIGHT", 100, None)
    repo, session = repository.FakeRepository(), FakeSession()
    services.add_batch(*batch, repo, session)
    services.allocate(*line, repo, session)

    assert session.committed is True

def test_allocate_returns_allocation():
    line = ("o1", "COMPLICATED-LAMP", 10)
    batch = ("b1", "COMPLICATED-LAMP", 100, None)
    session, repo = FakeSession(), repository.FakeRepository()
    services.add_batch(*batch, repo, session)

    result = services.allocate(*line, repo, FakeSession())

    assert result == "b1"

def test_add_batch_adds_a_batch_to_repository():
    batch = ('b1', 'BREAD-SWORD', 100, None)
    repo, session = repository.FakeRepository([]), FakeSession()
    services.add_batch(*batch, repo, session)
    assert session.committed is True
    assert repo.get('b1') is not None
