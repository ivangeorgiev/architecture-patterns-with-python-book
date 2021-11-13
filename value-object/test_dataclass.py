"""Implement Value Objects with Python dataclass.

We implement Value Object for Money which allows us to
compare, add and subtract money.
"""

import dataclasses
import pytest

@dataclasses.dataclass(frozen=True)
class Money:
    currency: str
    value: int

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f'Cannot add {self.currency} to {other.currency}')
        return Money(self.currency, self.value + other.value)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError(f'Cannot subtract {self.currency} from {other.currency}')
        if self.value < other.value:
            raise ValueError(f'Cannot subtract {self.value} from {other.value}. Value to subtract is too big.')
        return Money(self.currency, self.value - other.value)

    def __gt__(self, other):
        if self.currency != other.currency:
            raise ValueError(f'Cannot add {self.currency} to {other.currency}')
        return self.value > other.value

fiver = Money('gbp', 5)
tenner = Money('gbp', 10)
fiver_other = Money('usd', 5)

def test_immutable_dataclass_raises_error_on_update():
    with pytest.raises(dataclasses.FrozenInstanceError):
        fiver.value = 3

def test_equality():
    assert Money('gbp', 5) == Money('gbp', 5)

def test_money_with_different_currency_are_inequal():
    assert fiver != fiver_other

def test_adding_money_same_currency_adds_values():
    assert tenner == fiver + fiver

def test_adding_money_different_currency_raises_error():
    with pytest.raises(ValueError):
        _ = fiver + fiver_other
    

def test_subtract_money_same_currency_subtracts_values():
    assert tenner - fiver == fiver

def test_subtract_smaller_value_from_bigger_value_raises_error():
    with pytest.raises(ValueError):
        _ = fiver - tenner

def test_subtract_money_different_currency_raises_error():
    with pytest.raises(ValueError):
        _ = tenner - fiver_other

def test_compare_gt_money_same_currency_compares_value():
    assert tenner > fiver

def test_compare_gt_money_different_currency_raises_error():
    with pytest.raises(ValueError):
        _ = tenner > fiver_other

def test_compare_lt_money_same_currency_compares_value():
    assert fiver < tenner

