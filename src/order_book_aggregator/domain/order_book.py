from typing import NamedTuple

Order = NamedTuple("Order", [("price", float), ("size", float)])
OrderBookSide = NamedTuple("OrderBookSide", [("orders", list[Order])])
OrderBook = NamedTuple("OrderBook", [("bids", OrderBookSide), ("asks", OrderBookSide)])
