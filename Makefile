.PHONY: help lint format check type-check test all install setup sync

help:
	@echo "Available commands:"
	@echo "  sync        - Install dependencies with uv"
	@echo "  install     - Alias for sync"
	@echo "  lint        - Run ruff linting"
	@echo "  format      - Run ruff formatting"
	@echo "  check       - Run both linting and formatting"
	@echo "  type-check  - Run mypy type checking"
	@echo "  test        - Run pytest"
	@echo "  all         - Run all checks"
	@echo "  setup       - Setup pre-commit hooks"

sync:
	uv sync --group dev

install: sync

lint:
	uv run ruff check codepg/ tests/

format:
	uv run ruff format codepg/ tests/

check: lint format

type-check:
	uv run mypy codepg/

test:
	uv run pytest

all: check type-check test

setup:
	uv run pre-commit install
