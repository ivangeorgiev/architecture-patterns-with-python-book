"""Implement Value Object with Python NamedTuple.

We implement Value Object for Money which allows us to
compare, add and subtract money.
"""
import pytest
from typing import NamedTuple

class Money(NamedTuple):
    currency: str
    value: int

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f'Cannot add {self.currency} to different currency {other.currency}.')
        return Money(self.currency, self.value + other.value)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError(f'Cannot subtract {other.currency} from different currency {other.currency}.')
        if self.value < other.value:
            raise ValueError(f'Cannot subtract {other.value} from {self.value}. Value to subtract is too big.')
        return Money(self.currency, self.value - other.value)

    def __gt__(self, other):
        if self.currency != other.currency:
            raise ValueError(f'Cannot compare {other.currency} to differenty currency {other.currency}.')
        return self.value > other.value
    
zeroer = Money('gbp', 0)
fiver = Money('gbp', 5)
tenner = Money('gbp', 10)
fiver_other = Money('usd', 5)

def test_equality_same_currency_compares_value():
    assert Money('gbp', 5) == Money('gbp', 5)

def test_equality_different_currency_returns_false():
    assert fiver != fiver_other

def test_add_same_currency_adds_values():
    assert tenner == fiver + fiver

def test_add_different_currency_raises_error():
    with pytest.raises(ValueError):
        _ = fiver + fiver_other

def test_sub_same_currency_subtracts_values():
    assert fiver == tenner - fiver

def test_sub_different_currency_raises_error():
    with pytest.raises(ValueError):
        _ = tenner - fiver_other

def test_sub_same_currency_bigger_value_raises_error():
    with pytest.raises(ValueError):
        _ = fiver - tenner

def test_sub_same_currency_same_ammount_returns_zero_value():
    assert zeroer == fiver - Money('gbp', 5)

def test_gt_same_currency_returns_true_greater_value():
    assert tenner > fiver

def test_gt_same_currency_returns_false_smaller_value():
    assert not (fiver > tenner)

def test_gt_same_currency_returns_false_equal_value():
    assert not (tenner > Money('gbp', 10))

def test_gt_different_currency_raises_error():
    with pytest.raises(ValueError):
        _ = fiver > fiver_other

def test_lt_same_currency_returns_true_lower_value():
    assert fiver < tenner
