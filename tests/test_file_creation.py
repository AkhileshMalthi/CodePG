import pytest
import os
from pathlib import Path
import datetime
from codepg.app import create_file, get_file_template
from codepg.config import Config

def test_get_file_template():
    """Test getting file templates for different languages."""
    # Test Python template
    python_template = get_file_template("python", "test.py", "/path/folder")
    assert "def main():" in python_template
    assert "if __name__ == '__main__':" in python_template
    
    # Test JavaScript template
    js_template = get_file_template("javascript", "test.js", "/path/folder")
    assert "function main()" in js_template
    assert "main();" in js_template
    
    # Test fallback template
    fallback = get_file_template("unknown", "test.xyz", "/path/folder")
    assert "test.xyz created in /path/folder" in fallback

def test_create_file_python(temp_dir):
    """Test creating a Python file."""
    # Create a config with our temp directory
    config = Config()
    config.set("base_dir", str(temp_dir))
    
    # Create a python file
    file_path = create_file("hello.py", config)
    
    # Check that the file was created
    assert file_path is not None
    assert Path(file_path).exists()
    
    # Check the content
    with open(file_path, 'r') as f:
        content = f.read()
    
    assert "def main():" in content
    assert "if __name__ == '__main__':" in content

def test_create_file_structure(temp_dir):
    """Test the directory structure created for files."""
    config = Config()
    config.set("base_dir", str(temp_dir))
    
    # Create a JavaScript file
    file_path = create_file("script.js", config)
    assert file_path is not None
    
    # Check the directory structure
    file_path = Path(file_path)
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    assert file_path.name == "script.js"
    assert file_path.parent.name == today
    assert file_path.parent.parent.name == "javascript-playground"

def test_create_file_unsupported_extension(temp_dir):
    """Test creating a file with an unsupported extension."""
    config = Config()
    config.set("base_dir", str(temp_dir))
    
    # Try to create a file with unsupported extension
    file_path = create_file("test.unsupported", config)
    
    # Should return None for unsupported extension
    assert file_path is None

def test_create_file_existing(temp_dir):
    """Test behavior when creating a file that already exists."""
    config = Config()
    config.set("base_dir", str(temp_dir))
    
    # Create a file first time
    file_path1 = create_file("duplicate.py", config)
    assert file_path1 is not None
    
    # Get the content after first creation
    with open(file_path1, 'r') as f:
        original_content = f.read()
    
    # Modify the content
    with open(file_path1, 'w') as f:
        f.write("# Modified content\n")
    
    # Try to create the same file again
    file_path2 = create_file("duplicate.py", config)
    assert file_path2 == file_path1  # Should return the same path
    
    # Verify the content wasn't overwritten
    with open(file_path2, 'r') as f:
        new_content = f.read()
    
    assert new_content == "# Modified content\n"
    assert new_content != original_content
