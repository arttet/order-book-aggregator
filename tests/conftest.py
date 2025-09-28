import pytest

from order_book_aggregator.adapters import (
    fetch_coinbase_orderbook,
    fetch_gemini_orderbook,
)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    fetch_coinbase_orderbook.reset_rate_limit()
    fetch_gemini_orderbook.reset_rate_limit()
