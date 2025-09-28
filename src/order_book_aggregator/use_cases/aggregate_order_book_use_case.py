import asyncio

from order_book_aggregator.adapters import (
    fetch_coinbase_orderbook,
    fetch_gemini_orderbook,
)
from order_book_aggregator.domain import Side
from order_book_aggregator.use_cases.сalculate_execution_price_use_case import (
    calculate_execution_price_use_case,
)


async def aggregate_order_book_use_case(quantity: float) -> None:
    coinbase, gemini = await asyncio.gather(
        fetch_coinbase_orderbook(), fetch_gemini_orderbook()
    )
    order_books = [coinbase, gemini]

    buy_price = calculate_execution_price_use_case(
        order_books,
        quantity,
        side=Side.BUY,
    )

    sell_price = calculate_execution_price_use_case(
        order_books,
        quantity,
        side=Side.SELL,
    )

    print(f"To buy {quantity} BTC: ${buy_price:,.2f}")
    print(f"To sell {quantity} BTC: ${sell_price:,.2f}")
