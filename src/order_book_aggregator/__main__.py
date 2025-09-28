#!/usr/bin/env python3

import argparse
import asyncio

from order_book_aggregator.cli import positive_float
from order_book_aggregator.use_cases import aggregate_order_book_use_case


async def entrypoint(args: argparse.Namespace) -> None:
    await aggregate_order_book_use_case(quantity=args.qty)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="BTC-USD order book aggregator")
    parser.add_argument(
        "--qty", type=positive_float, default=10.0, help="quantity of BTC"
    )
    args = parser.parse_args(argv)

    asyncio.run(entrypoint(args))


if __name__ == "__main__":
    main()
