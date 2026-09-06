import json

from codepg.config import DEFAULT_CONFIG, Config


def test_config_defaults():
    """Test that config initializes with default values."""
    config = Config()
    assert config.base_dir == DEFAULT_CONFIG["base_dir"]
    assert config.editor_command == DEFAULT_CONFIG["editor_command"]
    assert config.loaded_from is None


def test_config_load_from_file(temp_config_file):
    """Test loading configuration from a file."""
    config = Config(config_path=str(temp_config_file))

    with open(temp_config_file) as f:
        expected_config = json.load(f)

    assert config.base_dir == expected_config["base_dir"]
    assert config.editor_command == expected_config["editor_command"]
    assert config.loaded_from == temp_config_file


def test_config_env_override(mock_env_vars):
    """Test environment variable overrides."""
    test_dir = "/test/env/dir"
    test_cmd = 'test-editor "{path}"'

    mock_env_vars("BASE_DIR", test_dir)
    mock_env_vars("EDITOR_COMMAND", test_cmd)

    config = Config()
    assert config.base_dir == test_dir
    assert config.editor_command == test_cmd


def test_config_env_config_path(temp_config_file, mock_env_vars):
    """Test loading config from path specified in environment variable."""
    mock_env_vars("CONFIG_FILE", str(temp_config_file))

    config = Config()
    assert config.loaded_from == temp_config_file


def test_config_save(temp_dir):
    """Test saving configuration to file."""
    config_path = temp_dir / "saved_config.json"
    config = Config()

    # Modify a setting
    config.set("base_dir", "/custom/path")

    # Save to the custom path
    success, message = config.save(config_path)

    assert success is True
    assert str(config_path) in message
    assert config_path.exists()

    # Load the saved config and verify
    with open(config_path) as f:
        saved_data = json.load(f)

    assert saved_data["base_dir"] == "/custom/path"


def test_config_create_default(temp_dir):
    """Test creating a default configuration file."""
    config_path = temp_dir / "default_config.json"

    success, message = Config.create_default_config(config_path)

    assert success is True
    assert str(config_path) in message
    assert config_path.exists()

    # Verify the contents
    with open(config_path) as f:
        created_config = json.load(f)

    assert created_config == DEFAULT_CONFIG


def test_config_get_set():
    """Test getting and setting configuration values."""
    config = Config()

    # Set a valid option
    assert config.set("base_dir", "/new/path") is True
    assert config.get("base_dir") == "/new/path"

    # Try to set an invalid option
    assert config.set("invalid_option", "value") is False

    # Get with default value
    assert config.get("nonexistent", "default") == "default"


def test_show_all():
    """Test retrieving all configuration options."""
    config = Config()
    config_data = config.show_all()

    # Should have the same keys as DEFAULT_CONFIG
    assert set(config_data.keys()) == set(DEFAULT_CONFIG.keys())

    # Should be a copy, not a reference
    config_data["test"] = "value"
    assert "test" not in config.show_all()
