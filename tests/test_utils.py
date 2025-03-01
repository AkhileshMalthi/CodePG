import pytest
import os
import platform
from codepg.utils import get_base_dir, get_supported_languages, detect_default_editor, is_command_available

def test_get_base_dir(mock_env_vars):
    """Test getting the base directory."""
    # Default case
    assert get_base_dir() == os.path.expanduser("~/CodePG")
    
    # With environment variable set
    test_dir = "/test/code/playgrounds"
    mock_env_vars("BASE_DIR", test_dir)
    assert get_base_dir() == test_dir

def test_get_supported_languages():
    """Test getting supported languages."""
    langs = get_supported_languages()
    
    # Check some common extensions
    assert langs['.py'] == 'python'
    assert langs['.js'] == 'javascript'
    assert langs['.java'] == 'java'
    
    # Make sure the dictionary has a reasonable size
    assert len(langs) > 10

@pytest.mark.parametrize("cmd,expected", [
    ("command_exists", True),
    ("command_doesnt_exist", False)
])
def test_is_command_available(cmd, expected, monkeypatch):
    """Test checking if commands are available."""
    from shutil import which
    
    def mock_which(command):
        return "/usr/bin/command" if command == "command_exists" else None
    
    # Mock the which function to control what commands "exist"
    monkeypatch.setattr("shutil.which", mock_which)
    
    assert is_command_available(cmd) == expected

@pytest.mark.parametrize("system,commands,expected_cmd", [
    ("windows", ["code"], "code"),
    ("windows", ["notepad"], "notepad"),
    ("darwin", ["code"], "code"),
    ("linux", ["vim"], "vim"),
    ("unknown", [], None)
])
def test_detect_default_editor(system, commands, expected_cmd, monkeypatch):
    """Test detecting the default editor."""
    # Mock platform.system
    monkeypatch.setattr(platform, "system", lambda: system)
    
    # Mock is_command_available to control which commands are "available"
    def mock_available(cmd):
        return cmd in commands
    
    monkeypatch.setattr("codepg.utils.is_command_available", mock_available)
    
    result = detect_default_editor()
    
    if expected_cmd is None:
        assert result is None
    else:
        # Instead of testing the exact format string, test that it:
        # 1. Contains the expected command
        # 2. Contains the path placeholder properly
        assert result is not None
        assert expected_cmd in result
        assert "{path}" in result
        
        # Test that the format string works correctly
        # This ensures that we're testing the actual functionality,
        # rather than the exact string format which might change
        formatted = result.format(path="test/path")
        assert expected_cmd in formatted
        assert "test/path" in formatted
