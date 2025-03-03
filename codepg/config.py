import os
import json
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv()

DEFAULT_CONFIG = {
    "base_dir": os.path.expanduser("~/CodePG"),
    "editor_command": "code \"{path}\"",
    "ai_model_type": "groq",  # can be "groq" or "ollama"
    "ai_model_name": None,    # default model will be used if not specified
    "groq_api_key": "",       # Remove hardcoded key, will be loaded from environment
    "use_crew_ai": False,     # whether to use CrewAI for more complex tasks
}

# Environment variable prefix for all configurable options
ENV_PREFIX = "CODEPG_"

class Config:
    """Configuration manager for CodePG application."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration.
        
        Parameters:
            config_path (Optional[str]): Path to the configuration file. If None, uses default locations.
        """
        self._config = DEFAULT_CONFIG.copy()
        self._loaded_from = None
        self._load_config(config_path)
        self._apply_env_overrides()
    
    def _load_config(self, config_path: Optional[str] = None) -> None:
        """
        Load configuration from file.
        
        Parameters:
            config_path (Optional[str]): Path to the configuration file. If None, uses default locations.
        """
        # Define default config file locations
        default_locations = self.get_default_config_locations()
        
        # If a specific path is provided, try it first
        if config_path:
            if self._try_load_config(Path(config_path)):
                return
            
        # Check environment variable for config path
        env_config_path = os.environ.get(f"{ENV_PREFIX}CONFIG_FILE")
        if env_config_path:
            if self._try_load_config(Path(env_config_path)):
                return
            
        # Try default locations
        for location in default_locations:
            if self._try_load_config(location):
                return
    
    @staticmethod
    def get_default_config_locations() -> List[Path]:
        """
        Get the default configuration file locations.
        
        Returns:
            List[Path]: List of paths to default configuration file locations.
        """
        return [
            Path("./codepg_config.json"),
            Path(os.path.expanduser("~/.config/codepg/config.json")),
            Path(os.path.expanduser("~/.codepg.json")),
        ]

    def _try_load_config(self, path: Path) -> bool:
        """
        Try to load configuration from a specific file.
        
        Parameters:
            path (Path): Path to the configuration file.
            
        Returns:
            bool: True if the configuration was loaded, False otherwise.
        """
        try:
            if path.exists():
                with open(path, 'r') as f:
                    user_config = json.load(f)
                    self._config.update(user_config)
                    self._loaded_from = path
                return True
        except Exception as e:
            print(f"Warning: Error loading config from {path}: {e}")
        return False
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to the configuration."""
        for key in DEFAULT_CONFIG:
            env_var = f"{ENV_PREFIX}{key.upper()}"
            if env_var in os.environ:
                self._config[key] = os.environ[env_var]
    
    @property
    def base_dir(self) -> str:
        """Get the base directory for code playgrounds."""
        return self._config.get('base_dir', DEFAULT_CONFIG['base_dir'])
    
    @property
    def editor_command(self) -> str:
        """Get the command to open the editor."""
        return self._config.get('editor_command', DEFAULT_CONFIG['editor_command'])
    
    @property
    def loaded_from(self) -> Optional[Path]:
        """Get the path from which the configuration was loaded."""
        return self._loaded_from
    
    def save(self, path: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Save the current configuration to a file.
        
        Parameters:
            path (Optional[Path]): Path to save the configuration to.
                                  If None, saves to the loaded location or the first default location.
                                  
        Returns:
            Tuple[bool, str]: (Success status, Message or path where saved)
        """
        save_path = path
        
        if save_path is None:
            if self._loaded_from is not None:
                save_path = self._loaded_from
            else:
                default_locations = self.get_default_config_locations()
                if default_locations:
                    save_path = default_locations[0]
                    # Create parent directory if it doesn't exist
                    if not save_path.parent.exists():
                        try:
                            save_path.parent.mkdir(parents=True, exist_ok=True)
                        except Exception as e:
                            return False, f"Failed to create directory {save_path.parent}: {e}"
        
        if save_path is None:
            return False, "No save path specified and no defaults available"
        
        try:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'w') as f:
                json.dump(self._config, f, indent=4)
            self._loaded_from = save_path
            return True, str(save_path)
        except Exception as e:
            return False, f"Failed to save configuration: {e}"
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration option.
        
        Parameters:
            key (str): The configuration key to set.
            value (Any): The value to set.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if key in DEFAULT_CONFIG:
            self._config[key] = value
            return True
        return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration option.
        
        Parameters:
            key (str): The configuration key to get.
            default (Any): The default value if the key is not found.
            
        Returns:
            Any: The configuration value, or the default if not found.
        """
        return self._config.get(key, default)
    
    def show_all(self) -> Dict[str, Any]:
        """
        Get all configuration options.
        
        Returns:
            Dict[str, Any]: Dictionary of all configuration options.
        """
        return self._config.copy()

    @classmethod
    def create_default_config(cls, path: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Create a default configuration file.
        
        Parameters:
            path (Optional[Path]): Path to create the configuration file.
                                 If None, uses the first default location.
                                 
        Returns:
            Tuple[bool, str]: (Success status, Message or path where created)
        """
        if path is None:
            default_locations = cls.get_default_config_locations()
            if default_locations:
                path = default_locations[0]
            else:
                return False, "No default configuration location available"
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            return True, str(path)
        except Exception as e:
            return False, f"Failed to create default configuration: {e}"
