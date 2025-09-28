import asyncio

import pytest

from order_book_aggregator.adapters import fetch_coinbase_orderbook
from order_book_aggregator.domain import OrderBook


@pytest.mark.asyncio
async def test_rate_limiter_no_exception_after_interval():
    await fetch_coinbase_orderbook()
    await asyncio.sleep(3)

    order_book = await fetch_coinbase_orderbook()
    assert isinstance(order_book, OrderBook)


@pytest.mark.asyncio
async def test_rate_limiter_raises_exception_when_too_soon():
    await fetch_coinbase_orderbook()
    with pytest.raises(Exception) as exc_info:
        await fetch_coinbase_orderbook()

    assert "Rate limit exceeded" in str(exc_info.value)
