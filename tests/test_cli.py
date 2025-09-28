import argparse

import pytest

from order_book_aggregator.cli import positive_float


def test_positive_float_valid():
    assert positive_float("1.5") == 1.5
    assert positive_float("10") == 10.0


def test_positive_float_zero_or_negative():
    with pytest.raises(
        argparse.ArgumentTypeError, match="Quantity must be greater than 0"
    ):
        positive_float("0")

    with pytest.raises(
        argparse.ArgumentTypeError, match="Quantity must be greater than 0"
    ):
        positive_float("-5")


def test_positive_float_invalid_string():
    with pytest.raises(
        argparse.ArgumentTypeError, match="Quantity must be a valid number"
    ):
        positive_float("abc")

    with pytest.raises(
        argparse.ArgumentTypeError, match="Quantity must be a valid number"
    ):
        positive_float("")
