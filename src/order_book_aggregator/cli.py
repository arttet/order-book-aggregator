import argparse


def positive_float(value):
    """Validate that the input is a positive float (> 0)."""
    try:
        qty = float(value)
        if qty <= 0:
            raise argparse.ArgumentTypeError(
                f"Quantity must be greater than 0, got {qty}"
            )
        return qty
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Quantity must be a valid number, got {value}"
        )
