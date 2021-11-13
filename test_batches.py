import datetime

import pytest

import model
from conftestlib import (
    BatchFactory,
    OrderlineFactory
)

@pytest.fixture()
def large_batch(batch_factory:BatchFactory):
    return batch_factory(qty=20)

@pytest.fixture()
def small_batch(batch_factory:BatchFactory):
    return batch_factory(qty=2)

@pytest.fixture()
def large_line(orderline_factory:OrderlineFactory):
    return orderline_factory(qty=20)

@pytest.fixture()
def small_line(orderline_factory:OrderlineFactory):
    return orderline_factory(qty=2)

def test_batch_has_reference(batch_factory:BatchFactory):
    batch = batch_factory(ref='b-55')
    assert 'b-55' == batch.reference

def test_batch_has_sku(batch_factory:BatchFactory):
    batch = batch_factory(sku='cucaracha')
    assert 'cucaracha' == batch.sku

def test_batch_has_available_quantity(batch_factory:BatchFactory):
    batch = batch_factory(qty=10)
    assert 10 == batch.available_quantity

def test_batch_has_eta(batch_factory:BatchFactory, tomorrow:datetime.date):
    batch = batch_factory(eta=tomorrow)
    assert tomorrow == batch.eta

def test_allocate_to_a_batch_reduces_the_available_quantity(batch_factory:BatchFactory, orderline_factory:OrderlineFactory):
    batch = batch_factory(qty=20)
    line = orderline_factory(qty=2)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required(large_batch, small_line):
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_smaller_than_required(small_batch, large_line):
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required(large_batch, large_line):
    assert large_batch.can_allocate(large_line)

def test_cannot_allocate_if_skus_do_not_match(batch_factory, orderline_factory):
    batch = batch_factory(sku='BLUE-PILL')
    line = orderline_factory(sku='RED-PILL')
    assert batch.can_allocate(line) is False


def test_can_only_deallocate_allocated_lines(batch_factory, orderline_factory):
    batch = batch_factory(qty=20)
    unallocated_line = orderline_factory(qty=2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

def test_allocate_is_idempotent(batch_factory:BatchFactory, orderline_factory:OrderlineFactory):
    batch = batch_factory(qty=20)
    line = orderline_factory(qty=2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_batches_are_equal_if_references_match_even_qty_doesnt_match(batch_factory:BatchFactory):
    batch_1 = batch_factory(ref='BATCH', qty=20)
    batch_2 = batch_factory(ref='BATCH', qty=5)
    assert batch_1 == batch_2

def test_batches_are_not_equal_if_references_are_different(batch_factory:BatchFactory):
    batch_1 = batch_factory(ref='BATCH-1', qty=20)
    batch_2 = batch_factory(ref='BATCH-2', qty=5)
    assert batch_1 != batch_2

def test_hash_returns_same_value_if_references_match(batch_factory: BatchFactory):
    batch_1 = batch_factory(ref='BATCH')
    batch_2 = batch_factory(ref='BATCH')
    assert hash(batch_1) == hash(batch_2)

def test_hash_returns_different_values_if_references_do_not_match(batch_factory: BatchFactory):
    batch_1 = batch_factory(ref='BATCH-1')
    batch_2 = batch_factory(ref='BATCH-2')
    assert hash(batch_1) != hash(batch_2)
