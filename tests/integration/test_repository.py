# pylint: disable=protected-access
import pytest

from domain import model
from adapters import repository


def test_repository_can_save_a_batch(db_session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    repo = repository.SqlAlchemyRepository(db_session)
    repo.add(batch)
    db_session.commit()

    rows = db_session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]

# @pytest.mark.skip()
def insert_order_line(db_session):
    db_session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = db_session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


# @pytest.mark.skip()
def insert_batch(db_session, batch_id):
    db_session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        dict(batch_id=batch_id),
    )
    [[batch_id]] = db_session.execute(
        'SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"',
        dict(batch_id=batch_id),
    )
    return batch_id


# @pytest.mark.skip()
def insert_allocation(db_session, orderline_id, batch_id):
    db_session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


# @pytest.mark.skip()
def test_repository_can_retrieve_a_batch_with_allocations(db_session):
    orderline_id = insert_order_line(db_session)
    batch1_id = insert_batch(db_session, "batch1")
    insert_batch(db_session, "batch2")
    insert_allocation(db_session, orderline_id, batch1_id)

    repo = repository.SqlAlchemyRepository(db_session)
    retrieved = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }

