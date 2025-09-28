import asyncio

from order_book_aggregator.adapters import (
    fetch_coinbase_orderbook,
    fetch_gemini_orderbook,
)

def setup_module():
    fetch_coinbase_orderbook.disable_rate_limit()
    fetch_gemini_orderbook.disable_rate_limit()


def test_benchmark_fetch_coinbase_orderbook(benchmark):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def sync_wrapper():
        return loop.run_until_complete(fetch_coinbase_orderbook())

    try:
        benchmark(sync_wrapper)
    finally:
        loop.close()
        asyncio.set_event_loop(None)


def test_benchmark_fetch_gemini_orderbook(benchmark):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def sync_wrapper():
        return loop.run_until_complete(fetch_gemini_orderbook())

    try:
        benchmark(sync_wrapper)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
