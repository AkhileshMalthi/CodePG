# Migration from Black/Flake8/isort to Ruff

This document explains the migration from the old linting and formatting tools to Ruff.

## What Changed

### Before (Multiple Tools)
- **Flake8**: For linting
- **Black**: For code formatting
- **isort**: For import sorting

### After (Single Tool)
- **Ruff**: For linting, formatting, and import sorting

## Configuration Migration

### Old Configuration Files (Removed)
- `.flake8` - Flake8 configuration
- `[tool.black]` in `pyproject.toml` - Black configuration  
- `[tool.isort]` in `pyproject.toml` - isort configuration

### New Configuration
- `[tool.ruff]` in `pyproject.toml` - All-in-one configuration
- `.ruff.toml` - Alternative standalone configuration file

## Command Migration

### Old Commands
```bash
# Linting
poetry run flake8 codepg/ tests/

# Formatting
poetry run black codepg/ tests/

# Import sorting
poetry run isort codepg/ tests/
```

### New Commands
```bash
# Linting
poetry run ruff check codepg/ tests/

# Formatting (includes import sorting)
poetry run ruff format codepg/ tests/

# Fix linting issues automatically
poetry run ruff check --fix codepg/ tests/
```

## Benefits of Ruff

1. **Speed**: 10-100x faster than the old tools
2. **Simplicity**: Single tool instead of three
3. **Compatibility**: Drop-in replacement with similar rules
4. **Features**: More built-in rules and better error messages

## Development Workflow

### Using Make
```bash
make lint      # Run linting
make format    # Run formatting
make check     # Run both
make all       # Run all checks including tests
```

### Using Python Script
```bash
python scripts/dev.py lint
python scripts/dev.py format
python scripts/dev.py check
python scripts/dev.py all
```

### Pre-commit Hooks
```bash
# Setup (one time)
make setup

# Hooks will run automatically on git commit
git commit -m "Your changes"
```

## CI/CD Changes

The GitHub Actions workflows have been updated to use Ruff instead of the old tools. The new workflow:

1. Installs dependencies (including Ruff)
2. Runs `ruff check` for linting
3. Runs `ruff format --check` to verify formatting
4. Runs MyPy for type checking

This is simpler and faster than the previous multi-tool approach.
