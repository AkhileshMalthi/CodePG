import os
import json
from typing import Optional, Dict, Any
from pathlib import Path

DEFAULT_CONFIG = {
    "base_dir": os.path.expanduser("~/CodePG"),
    "editor_command": "code \"{path}\"",
}

class Config:
    """Configuration manager for CodePG application."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration.
        
        Parameters:
            config_path (Optional[str]): Path to the configuration file. If None, uses default locations.
        """
        self._config = DEFAULT_CONFIG.copy()
        self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str] = None) -> None:
        """
        Load configuration from file.
        
        Parameters:
            config_path (Optional[str]): Path to the configuration file. If None, uses default locations.
        """
        # Define default config file locations
        default_locations = [
            Path("./codepg_config.json"),
            Path(os.path.expanduser("~/.config/codepg/config.json")),
            Path(os.path.expanduser("~/.codepg.json")),
        ]
        
        # If a specific path is provided, try it first
        if config_path:
            self._try_load_config(Path(config_path))
            return
            
        # Try default locations
        for location in default_locations:
            if self._try_load_config(location):
                return
    
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
                return True
        except Exception as e:
            print(f"Warning: Error loading config from {path}: {e}")
        return False
    
    @property
    def base_dir(self) -> str:
        """Get the base directory for code playgrounds."""
        return self._config.get('base_dir', DEFAULT_CONFIG['base_dir'])
    
    @property
    def editor_command(self) -> str:
        """Get the command to open the editor."""
        return self._config.get('editor_command', DEFAULT_CONFIG['editor_command'])
