import pytest

from allocation.domain import model
from tests.conftestlib import (
    BatchFactory,
    Eta,
    OrderlineFactory
)

def test_prefers_current_stock_batches_to_shipments(batch_factory:BatchFactory, orderline_factory:OrderlineFactory,
    tomorrow: Eta
):
    in_stock_batch = batch_factory(ref='IN-STOCK', sku='BLUE_RAY', qty=50, eta=None)
    shipment_batch = batch_factory(ref='IN-SHIPMENT', sku='BLUE_RAY', qty=50, eta=tomorrow)
    line = orderline_factory(sku='BLUE_RAY', qty=10)

    model.allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 40
    assert shipment_batch.available_quantity == 50

def test_prefers_earlier_batches(batch_factory:BatchFactory, orderline_factory:OrderlineFactory, 
                                 today: Eta, tomorrow: Eta, later:Eta):
    earliest = batch_factory(ref='EARLIEST', sku='BLUE_RAY', qty=100, eta=today)
    medium = batch_factory(ref='EARLIEST', sku='BLUE_RAY', qty=100, eta=tomorrow)
    latest = batch_factory(ref='EARLIEST', sku='BLUE_RAY', qty=100, eta=later)
    line = orderline_factory(sku='BLUE_RAY', qty=10)

    ref = model.allocate(line, [medium, earliest, latest])

    assert ref == 'EARLIEST'
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_retruns_allocated_batch_reference(
                                batch_factory:BatchFactory, orderline_factory:OrderlineFactory, 
                                today: Eta, tomorrow: Eta, later:Eta):
    in_stock = batch_factory(ref='IN_STOCK', sku='BLUE_RAY', qty=100, eta=None)
    in_shipment = batch_factory(ref='IN_SHIPMENT', sku='BLUE_RAY', qty=100, eta=tomorrow)
    line = orderline_factory(sku='BLUE_RAY', qty=10)

    ref = model.allocate(line, [in_shipment, in_stock])

    assert ref == 'IN_STOCK'

def test_raises_out_of_stock_exception_if_cannot_allocate(batch_factory:BatchFactory, orderline_factory:OrderlineFactory, today:Eta):
    batch = batch_factory(sku='CORN', qty=5, eta=today)
    line = orderline_factory(sku='CORN', qty=10)
    with pytest.raises(model.OutOfStock):
        model.allocate(line, [batch])
