import sys
from pathlib import Path
from unittest import mock

import pytest

from codepg.app import handle_config_command, main


@pytest.fixture
def mock_args():
    """Create mock args for testing."""

    class Args:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return Args


def test_main_no_args(capsys, monkeypatch):
    """Test main function when no arguments are provided."""
    # Mock sys.argv to provide no arguments
    monkeypatch.setattr(sys, "argv", ["codepg"])

    # Call main and check return code
    assert main() == 0

    # Check that help was printed
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "CodePG -" in captured.out


@mock.patch("codepg.app.create_file")
@mock.patch("codepg.app.open_in_editor")
def test_main_create_file(mock_open_editor, mock_create_file, temp_config_file, monkeypatch):
    """Test creating a file via main function."""
    # Setup
    mock_create_file.return_value = "/path/to/file.py"
    mock_open_editor.return_value = True

    # Mock sys.argv
    monkeypatch.setattr(
        sys, "argv", ["codepg", "create", "test.py", "--config", str(temp_config_file)]
    )

    # Run the command
    assert main() == 0

    # Check that our mocked functions were called properly
    mock_create_file.assert_called_once()
    assert mock_create_file.call_args[0][0] == "test.py"
    mock_open_editor.assert_called_once()


@mock.patch("codepg.app.create_file")
def test_main_create_file_failure(mock_create_file, monkeypatch):
    """Test behavior when file creation fails."""
    # Setup - simulate file creation failure
    mock_create_file.return_value = None

    # Mock sys.argv
    monkeypatch.setattr(sys, "argv", ["codepg", "create", "bad.file"])

    # Run the command - should return error code
    assert main() == 1

    # Verify create_file was called
    mock_create_file.assert_called_once()


@mock.patch("codepg.app.Config")
def test_config_show_command(mock_config_class, capsys, mock_args):
    """Test the 'config --show' command."""
    # Setup mock
    mock_config_instance = mock.MagicMock()
    mock_config_instance.show_all.return_value = {
        "base_dir": "/test/path",
        "editor_command": "test {path}",
    }
    mock_config_instance.loaded_from = "/path/to/config.json"
    mock_config_class.return_value = mock_config_instance

    # Create args
    args = mock_args(show=True, init=False, set=None, file=None, edit=False)

    # Run command
    assert handle_config_command(args) == 0

    # Check output
    captured = capsys.readouterr()
    assert "Current configuration:" in captured.out
    assert "base_dir: /test/path" in captured.out
    assert "editor_command: test {path}" in captured.out


@mock.patch("codepg.app.open_file_in_editor")
def test_config_edit_command(mock_open_file, mock_args):
    """Test the 'config --edit' command."""
    # Create a config instance with a loaded_from path
    mock_config = mock.MagicMock()
    mock_config.loaded_from = "/test/config.json"

    with mock.patch("codepg.app.Config", return_value=mock_config):
        # Create args
        args = mock_args(edit=True, init=False, show=False, set=None, file=None)

        # Run command
        assert handle_config_command(args) == 0

        # Check that editor was opened with config file
        mock_open_file.assert_called_once()
        assert mock_open_file.call_args[0][0] == "/test/config.json"


@mock.patch("codepg.app.Config.create_default_config")
def test_config_init_command(mock_create_default, mock_args):
    """Test the 'config --init' command."""
    # Setup mock
    mock_create_default.return_value = (True, "/path/to/new/config.json")

    # Create args
    args = mock_args(init=True, edit=False, show=False, set=None, file="/custom/path.json")

    # Run command
    assert handle_config_command(args) == 0

    # Check that create_default_config was called with the right path
    mock_create_default.assert_called_once()

    # Use Path objects to compare paths to handle different path separators across platforms
    expected_path = Path("/custom/path.json")
    actual_path = mock_create_default.call_args[0][0]
    assert Path(str(actual_path)) == expected_path
