import pytest

from order_book_aggregator.domain import Order, OrderBook, OrderBookSide, Side
from order_book_aggregator.use_cases import calculate_execution_price_use_case


class TestCalculateExecutionPrice:
    def setup_method(self):
        """
        Setup test data for each test
        """

        bids = [
            [1000.0, 1.0],
            [1001.0, 1.0],
            [1002.0, 1.0],
        ]

        asks = [
            [100.0, 1.0],
            [101.0, 1.0],
            [102.0, 1.0],
        ]

        bids_orders = [Order(price=price, size=size) for price, size in bids]
        asks_orders = [Order(price=price, size=size) for price, size in asks]

        bids_order_book_side = OrderBookSide(orders=bids_orders)
        asks_order_book_side = OrderBookSide(orders=asks_orders)

        order_book = OrderBook(bids=bids_order_book_side, asks=asks_order_book_side)
        self.order_books = [order_book]

    ###
    # Positive Test Cases (successful execution)
    ###

    @pytest.mark.parametrize(
        "volume,expected",
        [
            (0.0, 0.0),  # 0
            (0.5, 50.0),  # 0.5 * 100.0
            (1.0, 100.0),  # 1.0 * 100.0
            (1.5, 150.5),  # 1.0 * 100.0 + 0.5 * 101.0
            (2.0, 201.0),  # 1.0 * 100.0 + 1.0 * 101.0
            (2.5, 252.0),  # 1.0 * 100.0 + 1.0 * 101.0 + 0.5 * 102.0
            (3.0, 303.0),  # 1.0 * 100.0 + 1.0 * 101.0 + 1.0 * 102.0
        ],
    )
    def test_buy_parametrized_volumes(self, volume, expected):
        """
        Parametrized test for different buy volumes
        """
        result = calculate_execution_price_use_case(self.order_books, volume, Side.BUY)
        assert result == pytest.approx(expected)

    ###
    # Negative Test Cases (expect exceptions)
    ###

    def test_calculate_execution_price_invalid_order_books(self):
        with pytest.raises(ValueError, match="Invalid input parameters"):
            calculate_execution_price_use_case([], 1.0, Side.BUY)

    def test_calculate_execution_price_negative_quantity(self):
        with pytest.raises(ValueError, match="Invalid input parameters"):
            calculate_execution_price_use_case(self.order_books, -5.0, Side.SELL)

    def test_calculate_execution_price_not_enough_liquidity(self):
        order_book = OrderBook(
            bids=OrderBookSide(orders=[Order(price=100.0, size=1.0)]),
            asks=OrderBookSide(orders=[Order(price=101.0, size=1.0)]),
        )

        with pytest.raises(
            ValueError,
            match=r"Not enough liquidity to buy 2.0 BTC. Only 1.0 BTC available.",
        ):
            calculate_execution_price_use_case([order_book], 2.0, Side.BUY)

        with pytest.raises(
            ValueError,
            match=r"Not enough liquidity to sell 2.0 BTC. Only 1.0 BTC available.",
        ):
            calculate_execution_price_use_case([order_book], 2.0, Side.SELL)

    def test_order_book_side_empty(self):
        empty_buy_order_book = OrderBook(
            bids=OrderBookSide(orders=[Order(price=100.0, size=1.0)]),
            asks=OrderBookSide(orders=[]),
        )

        with pytest.raises(ValueError):
            calculate_execution_price_use_case([empty_buy_order_book], 1.0, Side.BUY)
