import argparse
import os
import datetime
import subprocess
from typing import Optional, Dict, Any
from pathlib import Path
import sys
import utils
from config import Config

def get_file_template(language: str, filename: str, folder_path: str) -> str:
    """
    Get the template for a specific programming language.
    
    Parameters:
        language (str): The programming language
        filename (str): The name of the file
        folder_path (str): The path to the folder containing the file
        
    Returns:
        str: The template string for the file
    """
    templates = {
        "python": f"# {filename}\n# Created: {datetime.date.today()}\n\n\ndef main():\n    pass\n\n\nif __name__ == '__main__':\n    main()\n",
        "javascript": f"// {filename}\n// Created: {datetime.date.today()}\n\nfunction main() {{\n    \n}}\n\nmain();\n",
        "typescript": f"// {filename}\n// Created: {datetime.date.today()}\n\nfunction main(): void {{\n    \n}}\n\nmain();\n",
        "rust": f"// {filename}\n// Created: {datetime.date.today()}\n\nfn main() {{\n    println!(\"Hello, world!\");\n}}\n",
        "go": f"// {filename}\n// Created: {datetime.date.today()}\n\npackage main\n\nimport \"fmt\"\n\nfunc main() {{\n    fmt.Println(\"Hello, world!\")\n}}\n",
        "java": f"// {filename}\n// Created: {datetime.date.today()}\n\npublic class {os.path.splitext(filename)[0]} {{\n    public static void main(String[] args) {{\n        System.out.println(\"Hello, world!\");\n    }}\n}}\n",
    }
    
    return templates.get(language.lower(), f"# {filename} created in {folder_path}\n")


def create_file(filename: str, config: Config) -> Optional[str]:
    """
    Create a new file for the specified programming language in a date-specific folder.

    Parameters:
        filename (str): The name of the file to be created (including extension).
        config (Config): Configuration object with settings.
        
    Returns:
        Optional[str]: Path to the created file or None if creation failed.
    """
    try:
        # Extract the file extension
        extension = Path(filename).suffix.lower()

        # Get today's date in YYYY-MM-DD format
        today = datetime.date.today().strftime("%Y-%m-%d")

        # Get the language based on the extension
        supported_extensions = utils.get_supported_languages()
        language = supported_extensions.get(extension, '')

        # Check if the extension is supported
        if not language:
            print(f"Error: Unsupported file extension: {extension}")
            print(f"Supported extensions: {', '.join(supported_extensions.keys())}")
            return None

        # Construct paths for the playground and today's folder
        playground_folder = Path(config.base_dir) / f"{language}-playground"
        today_folder = playground_folder / today

        # Create the directories if they do not exist
        today_folder.mkdir(parents=True, exist_ok=True)

        # Construct the full file path
        file_path = today_folder / filename

        # Create the file if it does not exist, and write a template inside it
        if not file_path.exists():
            with open(file_path, 'w') as file:
                file.write(get_file_template(language, filename, str(today_folder)))
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

        return str(file_path)

    except OSError as e:
        print(f"Error creating directories: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None


def open_in_editor(path: str, config: Config) -> bool:
    """
    Open the specified path in the configured code editor.
    
    Parameters:
        path (str): Path to open in the editor.
        config (Config): Configuration object with editor settings.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    editor_cmd = config.editor_command
    
    if not editor_cmd:
        print("No editor command configured. Skipping editor launch.")
        return False
        
    try:
        # Format the command with the path
        cmd = editor_cmd.format(path=path)
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to open editor. Command '{cmd}' returned non-zero exit status {e.returncode}")
        return False
    except Exception as e:
        print(f"Error opening editor: {e}")
        return False


def main() -> int:
    """
    Main function to handle command line arguments and execute program logic.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="CodePG - A CLI application to automate coding playground setup")
    
    # Add arguments
    parser.add_argument("filename", type=str, help="The name of the file to be created (including extension).")
    parser.add_argument("--config", "-c", type=str, help="Path to the configuration file.")
    parser.add_argument("--no-editor", action="store_true", help="Don't open the editor after creating the file.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = Config(config_path=args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return 1
    
    # Call create_file function with the parsed filename
    created_path = create_file(args.filename, config)
    if not created_path:
        return 1
        
    # Open the editor if not disabled
    if not args.no_editor:
        today_folder = str(Path(created_path).parent)
        if not open_in_editor(today_folder, config):
            print("Warning: Failed to open editor but file was created successfully.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
