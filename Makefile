.PHONY: help lint format check type-check test all install setup

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  lint        - Run ruff linting"
	@echo "  format      - Run ruff formatting"
	@echo "  check       - Run both linting and formatting"
	@echo "  type-check  - Run mypy type checking"
	@echo "  test        - Run pytest"
	@echo "  all         - Run all checks"
	@echo "  setup       - Setup pre-commit hooks"

install:
	poetry install

lint:
	poetry run ruff check codepg/ tests/

format:
	poetry run ruff format codepg/ tests/

check: lint format

type-check:
	poetry run mypy codepg/

test:
	poetry run pytest

all: check type-check test

setup:
	pre-commit install
