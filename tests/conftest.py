import datetime
import os

from flask.helpers import url_for

import pytest
from sqlalchemy.orm import sessionmaker

from allocation.domain import model
from allocation.entrypoints.flask_app import create_app

@pytest.fixture
def db_url_tmpdir(tmpdir):
    db_path = os.path.join(tmpdir, 'db.sqlite')
    return f'sqlite:///{db_path}'

@pytest.fixture
def db_url_memory():
    return 'sqlite:///:memory:'

@pytest.fixture
def app(db_url_memory):
    app = create_app({
        'TESTING': True,
        'DATABASE_URL': db_url_memory,
    })
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def db(app):
    return app.db

@pytest.fixture
def db_session_factory(db):
    yield sessionmaker(bind=db)

@pytest.fixture
def db_session(db_session_factory):
    yield db_session_factory()


@pytest.fixture
def add_stock(client):
    def _add_stock(lines):
        url = url_for('add_batch')
        fields = ('ref', 'sku', 'qty', 'eta')
        for line in lines:
            data = dict(zip(fields, line))
            r = client.post(url, json=data)
            assert r.status_code == 201
    return _add_stock

@pytest.fixture
def add_stock1(db_session):
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            db_session.execute(
                "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
                " VALUES (:ref, :sku, :qty, :eta)",
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            [[batch_id]] = db_session.execute(
                "SELECT id FROM batches WHERE reference=:ref AND sku=:sku",
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        db_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        db_session.execute(
            "DELETE FROM allocations WHERE batch_id=:batch_id",
            dict(batch_id=batch_id),
        )
        db_session.execute(
            "DELETE FROM batches WHERE id=:batch_id", dict(batch_id=batch_id),
        )
    for sku in skus_added:
        db_session.execute(
            "DELETE FROM order_lines WHERE sku=:sku", dict(sku=sku),
        )
        db_session.commit()


@pytest.fixture
def restart_api():
    pass



@pytest.fixture(scope='session')
def batch_factory():
    def _batch_factory(ref=None, sku=None, qty=None, eta=None):
        ref = ref or 'batch-01'
        sku = sku or 'FAKE-LAMP'
        qty = qty or 20
        return model.Batch(ref, sku, qty, eta)
    return _batch_factory

@pytest.fixture(scope='session')
def orderline_factory():
    def _factory(orderid=None, sku=None, qty=None):
        orderid = orderid or 'ORDER-REF'
        sku = sku or 'FAKE-LAMP'
        qty = qty or 2
        return model.OrderLine(orderid, sku, qty)
    return _factory

@pytest.fixture(scope='session')
def orderline(orderline_factory):
    return orderline_factory()

@pytest.fixture(scope='session')
def date_factory():
    def _date_factory(base_day=None, days_since=None):
        base_day = base_day or datetime.date.today()
        days_since = days_since or 0
        result = base_day + datetime.timedelta(days=days_since)
        return result
    return _date_factory

@pytest.fixture(scope='session')
def today(date_factory):
    return date_factory(days_since=0)

@pytest.fixture(scope='session')
def tomorrow(date_factory):
    return date_factory(days_since=1)

@pytest.fixture(scope='session')
def later(date_factory):
    return date_factory(days_since=5)

