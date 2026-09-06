# Development task runner script for CodePG
# Run with: uv run python scripts/dev.py <command>  or  python scripts/dev.py <command>

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> int:
    """Run a command and return the exit code."""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def main() -> int:
    """Main entry point for development tasks."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/dev.py <command>")
        print("Commands:")
        print("  lint        - Run ruff linting")
        print("  format      - Run ruff formatting")
        print("  check       - Run both linting and formatting")
        print("  type-check  - Run mypy type checking")
        print("  test        - Run pytest")
        print("  all         - Run all checks")
        print("  setup       - Setup pre-commit hooks")
        sys.exit(1)

    command = sys.argv[1]

    if command == "lint":
        return run_command(["uv", "run", "ruff", "check", "codepg/", "tests/"], "Ruff linting")

    elif command == "format":
        return run_command(
            ["uv", "run", "ruff", "format", "codepg/", "tests/"], "Ruff formatting"
        )

    elif command == "check":
        lint_code = run_command(
            ["uv", "run", "ruff", "check", "codepg/", "tests/"], "Ruff linting"
        )
        format_code = run_command(
            ["uv", "run", "ruff", "format", "codepg/", "tests/"], "Ruff formatting"
        )
        return max(lint_code, format_code)

    elif command == "type-check":
        return run_command(["uv", "run", "mypy", "codepg/"], "MyPy type checking")

    elif command == "test":
        return run_command(["uv", "run", "pytest"], "Running tests")

    elif command == "all":
        commands = [
            (["uv", "run", "ruff", "check", "codepg/", "tests/"], "Ruff linting"),
            (["uv", "run", "ruff", "format", "codepg/", "tests/"], "Ruff formatting"),
            (["uv", "run", "mypy", "codepg/"], "MyPy type checking"),
            (["uv", "run", "pytest"], "Running tests"),
        ]

        exit_codes = []
        for cmd, desc in commands:
            exit_codes.append(run_command(cmd, desc))

        return max(exit_codes)

    elif command == "setup":
        return run_command(["uv", "run", "pre-commit", "install"], "Setting up pre-commit hooks")

    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
