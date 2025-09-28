import time
from functools import wraps
from typing import Callable

import aiohttp
import orjson

from order_book_aggregator.domain import Order, OrderBook, OrderBookSide


def async_rate_limiter(min_interval: float):
    def decorator(func: Callable) -> Callable:
        last_call_time = [0.0]
        interval = [min_interval]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if interval[0] > 0:
                current_time = time.monotonic()
                elapsed = current_time - last_call_time[0]

                if elapsed < interval[0]:
                    func_name = getattr(func, "__name__", "unknown_function")
                    wait_time = min_interval - elapsed
                    raise Exception(
                        f"Rate limit exceeded for {func_name}. "
                        f"Must wait {wait_time:.2f} more seconds."
                    )

                last_call_time[0] = current_time

            return await func(*args, **kwargs)

        def reset_rate_limit():
            last_call_time[0] = 0.0

        def disable_rate_limit():
            interval[0] = 0.0


        wrapper.reset_rate_limit = reset_rate_limit
        wrapper.disable_rate_limit = disable_rate_limit

        return wrapper

    return decorator


def build_session() -> aiohttp.ClientSession:
    conn = aiohttp.TCPConnector(
        limit=1,
        limit_per_host=1,
        keepalive_timeout=30,
    )

    timeout = aiohttp.ClientTimeout(total=5, connect=1, sock_read=2)

    return aiohttp.ClientSession(
        connector=conn, timeout=timeout, json_serialize=orjson.dumps
    )


@async_rate_limiter(min_interval=2.0)
async def fetch_coinbase_orderbook(
    url: str = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2",
) -> OrderBook:
    async with build_session() as session:
        async with session.get(url, raise_for_status=True) as response:
            data = await response.json()

    bids_orders = [
        Order(price=float(price), size=float(size)) for price, size, _ in data["bids"]
    ]
    asks_orders = [
        Order(price=float(price), size=float(size)) for price, size, _ in data["asks"]
    ]

    bids_orders.sort(key=lambda order: order.price, reverse=True)
    asks_orders.sort(key=lambda order: order.price)

    return OrderBook(
        bids=OrderBookSide(orders=bids_orders), asks=OrderBookSide(orders=asks_orders)
    )


@async_rate_limiter(min_interval=2.0)
async def fetch_gemini_orderbook(
    url: str = "https://api.gemini.com/v1/book/BTCUSD",
) -> OrderBook:
    async with build_session() as session:
        async with session.get(url, raise_for_status=True) as response:
            data = await response.json()

    bids_orders = [
        Order(price=float(entry["price"]), size=float(entry["amount"]))
        for entry in data["bids"]
    ]

    asks_orders = [
        Order(price=float(entry["price"]), size=float(entry["amount"]))
        for entry in data["asks"]
    ]

    bids_orders.sort(key=lambda order: order.price, reverse=True)
    asks_orders.sort(key=lambda order: order.price)

    return OrderBook(
        bids=OrderBookSide(orders=bids_orders), asks=OrderBookSide(orders=asks_orders)
    )
