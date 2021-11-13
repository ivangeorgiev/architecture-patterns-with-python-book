import dataclasses
import datetime
import typing

class OutOfStock(Exception):
    pass

@dataclasses.dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(self, ref:str, sku:str, qty: int, eta: typing.Optional[datetime.date]):
        self.reference = ref
        self.sku = sku
        self._purchased_qantity = qty
        self._allocations = set() # type: typing.Set[OrderLine]
        self.eta = eta

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_qantity - self.allocated_quantity

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self.allocations.remove(line)
            return True
        return False
    def allocate(self, line:OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def can_allocate(self, line:OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other):
        if isinstance(other, Batch):
            return other.reference == self.reference
        return False

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(line: OrderLine, batches: typing.List[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f'Cannot allocate sku {line.sku}. Out of stock.')
    batch.allocate(line)
    return batch.reference
