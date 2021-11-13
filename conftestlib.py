import datetime
import typing

import model

Ref = typing.NewType('Ref', str)
Sku = typing.NewType('Sku', str)
Qty = typing.NewType('Qty', int)
Eta = typing.NewType('Eta', datetime.date)
BatchFactory = typing.Callable[[typing.Optional[Ref],typing.Optional[Sku],typing.Optional[Qty],typing.Optional[Eta]],model.Batch]
OrderlineFactory = typing.Callable[[typing.Optional[Ref],typing.Optional[Sku],typing.Optional[Qty]], model.OrderLine]
