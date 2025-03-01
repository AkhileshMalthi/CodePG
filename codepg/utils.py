import os
import platform
from typing import Dict, Optional

def get_base_dir() -> str:
    """
    Get the base directory for code playgrounds.
    
    Returns:
        str: Path to the base directory.
    """
    # Default base directory is in the user's home directory
    base_dir = os.path.expanduser("~/CodePG")
    
    # Check if environment variable is set
    if "CODEPG_BASE_DIR" in os.environ:
        base_dir = os.environ["CODEPG_BASE_DIR"]
    
    return base_dir

def get_supported_languages() -> Dict[str, str]:
    """
    Get a dictionary mapping file extensions to language names.
    
    Returns:
        Dict[str, str]: Dictionary mapping extensions to language names.
    """
    return {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.go': 'go',
        '.rs': 'rust',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.java': 'java',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.sh': 'shell',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.r': 'r',
        '.sql': 'sql',
        '.lua': 'lua',
        '.dart': 'dart',
    }

def detect_default_editor() -> Optional[str]:
    """
    Detect the default editor command for the current platform.
    
    Returns:
        Optional[str]: Command to launch the default code editor, or None if detection fails.
    """
    system = platform.system().lower()
    
    # Try to find VSCode first as it's common across platforms
    for vscode_cmd in ["code", "code-insiders"]:
        if is_command_available(vscode_cmd):
            return f'{vscode_cmd} "{{path}}"'
    
    # Platform-specific defaults
    if system == "windows":
        if is_command_available("notepad"):
            return 'notepad "{path}"'
    elif system == "darwin":  # macOS
        if is_command_available("open"):
            return 'open -a TextEdit "{path}"'
    else:  # Linux and others
        for editor in ["nano", "vim", "gedit", "xed"]:
            if is_command_available(editor):
                return f'{editor} "{{path}}"'
    
    return None

def is_command_available(cmd: str) -> bool:
    """
    Check if a command is available in the system.
    
    Parameters:
        cmd (str): The command to check.
        
    Returns:
        bool: True if the command is available, False otherwise.
    """
    try:
        from shutil import which
        return which(cmd) is not None
    except ImportError:
        # Fallback method for older Python versions
        import subprocess
        try:
            devnull = open(os.devnull, 'w')
            if platform.system().lower() == "windows":
                subprocess.check_call(f"where {cmd}", stdout=devnull, stderr=devnull, shell=True)
            else:
                subprocess.check_call(f"which {cmd}", stdout=devnull, stderr=devnull, shell=True)
            return True
        except subprocess.CalledProcessError:
            return False