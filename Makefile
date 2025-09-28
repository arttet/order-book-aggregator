.DEFAULT_GOAL := help

################################################################################

TEST_EXTRA_ARGS ?=
BENCH_EXTRA_ARGS ?= --benchmark-min-rounds=3
SCRIPT_EXTRA_ARGS ?=

export PYTHONPATH=src

################################################################################

# Note: use Makefile.local for customization
-include Makefile.local

################################################################################

## ▸▸▸ Development commands ◂◂◂

.PHONY: help
help:			## Show this help
	@fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/## //'

.PHONY: venv
venv:			## Create a virtual environment
	uv venv --clear

.PHONY: deps
deps:			## Install dependencies
	uv sync --frozen

.PHONY: audit
audit:			## Audit dependencies
	uv run pip-audit --strict --fix ${CURDIR}

.PHONY: fmt
fmt:			## Format code
	uv run isort .
	uv run ruff format

.PHONY: lint
lint:			## Lint code
	uv pip check
	uv lock --check
	uv run ty check --error-on-warning
	uv run ruff check --fix

.PHONY: build
build: fmt lint
build:			## Build the Python package distribution (wheel/sdist)
	uv build

.PHONY: test
test:			## Run tests with coverage
	uv run pytest --benchmark-disable --cov=order_book_aggregator --cov-report=term-missing ${TEST_EXTRA_ARGS}

.PHONY: bench
bench:			## Run benchmarks
	uv run pytest --benchmark-only --benchmark-save-data --benchmark-histogram=order_books_bench ${BENCH_EXTRA_ARGS}

.PHONY: install
install:		## Install the project in development mode
	uv pip install -e .

.PHONY: run
run:			## Run a script
	uv run python -m order_book_aggregator ${SCRIPT_EXTRA_ARGS}

.PHONY: cli
cli:			## Run a CLI script
	order-book-aggregator ${SCRIPT_EXTRA_ARGS}

.PHONY: clean
clean:			## Remove generated artifacts
	rm -rf .benchmarks
	rm -rf .pytest_cache
	rm -rf .venv
	rm -rf .ruff_cache
	rm -rf build
	rm -rf htmlcov
	rm -rf dist
	rm -rf .coverage

#######################################################################################################################
