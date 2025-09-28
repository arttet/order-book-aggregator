# Order Book Aggregator

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
venv:                   Create a Virtual Environment
deps:                   Install Dependencies
fmt:                    Format Code
lint:                   Lint Code
test:                   Run tests with coverage
run:                    Run a Script
```
