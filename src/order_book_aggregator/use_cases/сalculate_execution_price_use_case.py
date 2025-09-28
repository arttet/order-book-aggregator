import heapq

from order_book_aggregator.domain import OrderBook, Side


def calculate_execution_price_use_case(
    order_books: list[OrderBook],
    quantity: float,
    side: Side = Side.BUY,
) -> float:
    """
    Calculate the execution price of BTC using a k-way merge algorithm.

    Complexity: O(Q log k) where Q is quantity to fill, k is number of exchanges.
    Space: O(k) - only k elements in heap at any time.

    Args:
        order_books: List of order books from different exchanges
        quantity: Quantity to execute
        side: BUY or SELL

    Returns:
        Total execution cost

    Raises:
        ValueError: If invalid input parameters
        ValueError: If not enough liquidity available
    """

    if not order_books or quantity < 0:
        raise ValueError("Invalid input parameters")

    heap = []
    exchange_indexes = []

    # Initialize: put first order from each exchange into heap
    for exchange_idx, order_book in enumerate(order_books):
        order_book_side = order_book.asks if side == Side.BUY else order_book.bids

        if order_book_side.orders:
            price, size = order_book_side.orders[0]
            # For BUY: min-heap (best = lowest price)
            # For SELL: max-heap via negation (best = highest price)
            heap_price = price if side == Side.BUY else -price
            order_idx = 0

            heapq.heappush(heap, (heap_price, size, exchange_idx, order_idx))
            exchange_indexes.append(1)
        else:
            exchange_indexes.append(0)

    remaining_quantity = quantity
    total_cost = 0.0

    # Main k-way merge loop
    while remaining_quantity > 0 and heap:
        heap_price, available_size, exchange_idx, order_idx = heapq.heappop(heap)
        actual_price = heap_price if side == Side.BUY else -heap_price

        take_size = min(remaining_quantity, available_size)
        total_cost += take_size * actual_price
        remaining_quantity -= take_size

        if available_size > take_size:
            remaining_size = available_size - take_size
            heapq.heappush(heap, (heap_price, remaining_size, exchange_idx, order_idx))
        else:
            current_order_book = order_books[exchange_idx]
            order_book_side = (
                current_order_book.asks if side == Side.BUY else current_order_book.bids
            )
            next_order_idx = exchange_indexes[exchange_idx]

            if next_order_idx < len(order_book_side.orders):
                next_price, next_size = order_book_side.orders[next_order_idx]
                next_heap_price = next_price if side == Side.BUY else -next_price
                heapq.heappush(
                    heap, (next_heap_price, next_size, exchange_idx, next_order_idx)
                )
                exchange_indexes[exchange_idx] += 1

    if remaining_quantity > 0:
        executed_qty = quantity - remaining_quantity
        raise ValueError(
            f"Not enough liquidity to {side.value} {quantity} BTC. "
            f"Only {executed_qty} BTC available."
        )

    return total_cost
