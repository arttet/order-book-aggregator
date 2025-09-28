# Order Book Aggregator

[![build](https://github.com/arttet/order-book-aggregator/actions/workflows/build.yml/badge.svg)](https://github.com/arttet/order-book-aggregator/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/arttet/order-book-aggregator/graph/badge.svg?token=OMRV68FALD)](https://codecov.io/gh/arttet/order-book-aggregator)

Backend Challenge: Order Book Aggregator

## Installation

Before installing the `order-book-aggregator` package, you need to have `uv` installed.
`uv` is a Python dependency and package manager required to work with this project.

Once `uv` is installed, run:

```sh
uv pip install .
```

This will install the package and make the command-line script available.

Run with a specific quantity:

```sh
order-book-aggregator --qty 5
```

## Usage

After installation, you can run:

```sh
order-book-aggregator --help
usage: order-book-aggregator [-h] [--qty QTY]

BTC-USD order book aggregator

options:
  -h, --help  show this help message and exit
  --qty QTY   quantity of BTC
```

## Command Overview

```sh
$ make
▸▸▸ Development commands ◂◂◂
help:                   Show this help
venv:                   Create a virtual environment
deps:                   Install dependencies
audit:                  Audit dependencies
fmt:                    Format code
lint:                   Lint code
build:                  Build the Python package distribution (wheel/sdist)
test:                   Run tests with coverage
bench:                  Run benchmarks
install:                Install the project in development mode
run:                    Run a script
cli:                    Run a CLI script
clean:                  Remove generated artifacts
```
