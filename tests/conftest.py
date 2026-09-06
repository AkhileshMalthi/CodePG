import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_config_file(temp_dir):
    """Create a temporary configuration file."""
    config_path = temp_dir / "config.json"
    config_data = {
        "base_dir": str(temp_dir / "code_playgrounds"),
        "editor_command": 'echo "{path}"',  # Safe command for testing
    }

    with open(config_path, "w") as f:
        json.dump(config_data, f)

    return config_path


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    # Store original environment variables
    original_vars = {}
    for var in ["CODEPG_BASE_DIR", "CODEPG_EDITOR_COMMAND", "CODEPG_CONFIG_FILE"]:
        if var in os.environ:
            original_vars[var] = os.environ[var]

    # Allow tests to set variables
    def _set_env(name, value):
        monkeypatch.setenv(f"CODEPG_{name.upper()}", value)

    yield _set_env

    # Clean up (handled by monkeypatch fixture automatically)


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Mock the subprocess.run function."""

    class MockCompletedProcess:
        def __init__(self, returncode=0):
            self.returncode = returncode

    def mock_run(*args, **kwargs):
        check = kwargs.get("check", False)
        command = args[0] if args else kwargs.get("args", ["echo"])

        # Simulate a successful command by default
        returncode = 0

        # Optionally, tests can make specific commands fail
        if isinstance(command, str) and "fail_command" in command:
            returncode = 1
            if check:
                raise subprocess.CalledProcessError(returncode, command)

        return MockCompletedProcess(returncode=returncode)

    import subprocess

    monkeypatch.setattr(subprocess, "run", mock_run)
