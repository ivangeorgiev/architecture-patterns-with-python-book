import datetime

import pytest

import model

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

