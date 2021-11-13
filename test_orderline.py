import pytest

def test_orderline_has_order_id(orderline_factory):
    orderline = orderline_factory(orderid='order-000')
    assert 'order-000' == orderline.orderid

def test_orderline_has_sku(orderline_factory):
    orderline = orderline_factory(sku='BLUE-SKY')
    assert 'BLUE-SKY' == orderline.sku

def test_orderline_has_quantity(orderline_factory):
    orderline = orderline_factory(qty=5)
    assert 5 == orderline.qty

