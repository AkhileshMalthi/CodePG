import argparse
import datetime
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from codepg import utils
from codepg.config import Config
from codepg.logger import setup_logger

# Set up module logger
logger = setup_logger(__name__)


def _sanitize_java_class(name: str) -> str:
    """Sanitize filename stem into a valid Java class name."""
    stem = name.strip()
    # Replace invalid chars with underscore, ensure starts with letter/underscore
    sanitized = re.sub(r"[^A-Za-z0-9_]", "_", stem)
    if not sanitized:
        sanitized = "Main"
    if sanitized[0].isdigit():
        sanitized = f"_{sanitized}"
    # Capitalize first letter
    return sanitized[0].upper() + sanitized[1:] if len(sanitized) > 1 else sanitized.upper()


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
    today = datetime.date.today()
    java_class = _sanitize_java_class(Path(filename).stem)
    templates = {
        "python": f"# {filename}\n# Created: {today}\n\n\ndef main():\n    pass\n\n\nif __name__ == '__main__':\n    main()\n",
        "javascript": f"// {filename}\n// Created: {today}\n\nfunction main() {{\n    \n}}\n\nmain();\n",
        "typescript": f"// {filename}\n// Created: {today}\n\nfunction main(): void {{\n    \n}}\n\nmain();\n",
        "rust": f'// {filename}\n// Created: {today}\n\nfn main() {{\n    println!("Hello, world!");\n}}\n',
        "go": f'// {filename}\n// Created: {today}\n\npackage main\n\nimport "fmt"\n\nfunc main() {{\n    fmt.Println("Hello, world!")\n}}\n',
        "java": f'// {filename}\n// Created: {today}\n\npublic class {java_class} {{\n    public static void main(String[] args) {{\n        System.out.println("Hello, world!");\n    }}\n}}\n',
        "c": f'// {filename}\n// Created: {today}\n\n#include <stdio.h>\n\nint main() {{\n    printf("Hello, world!\\n");\n    return 0;\n}}\n',
        "cpp": f'// {filename}\n// Created: {today}\n\n#include <iostream>\n\nint main() {{\n    std::cout << "Hello, world!" << std::endl;\n    return 0;\n}}\n',
        "html": f"<!-- {filename} -->\n<!-- Created: {today} -->\n\n<!DOCTYPE html>\n<html>\n<head>\n    <title>{filename}</title>\n</head>\n<body>\n    <h1>Hello, world!</h1>\n</body>\n</html>\n",
        "css": f"/* {filename} */\n/* Created: {today} */\n\nbody {{\n    margin: 0;\n    padding: 0;\n}}\n",
        "shell": f'# {filename}\n# Created: {today}\n\n#!/bin/bash\n\necho "Hello, world!"\n',
        "sql": f"-- {filename}\n-- Created: {today}\n\nSELECT 'Hello, world!';\n",
        "ruby": f"# {filename}\n# Created: {today}\n\ndef main\n  puts 'Hello, world!'\nend\n\nmain\n",
        "php": f'<?php\n// {filename}\n// Created: {today}\n\necho "Hello, world!";\n',
        "csharp": f'// {filename}\n// Created: {today}\n\nusing System;\n\nclass Program {{\n    static void Main() {{\n        Console.WriteLine("Hello, world!");\n    }}\n}}\n',
        "swift": f'// {filename}\n// Created: {today}\n\nimport Foundation\n\nprint("Hello, world!")\n',
        "kotlin": f'// {filename}\n// Created: {today}\n\nfun main() {{\n    println("Hello, world!")\n}}\n',
        "dart": f"// {filename}\n// Created: {today}\n\nvoid main() {{\n  print('Hello, world!');\n}}\n",
        "lua": f'-- {filename}\n-- Created: {today}\n\nprint("Hello, world!")\n',
        "r": f'# {filename}\n# Created: {today}\n\nprint("Hello, world!")\n',
    }

    return templates.get(language.lower(), f"# {filename} created in {folder_path}\n")


def create_file(filename: str, config: Config) -> str | None:
    """
    Create a new file for the specified programming language in a date-specific folder.

    Parameters:
        filename (str): The name of the file to be created (including extension).
        config (Config): Configuration object with settings.

    Returns:
        Optional[str]: Path to the created file or None if creation failed.
    """
    try:
        # Validate filename does not contain path traversal
        if (
            Path(filename).name != filename
            or ".." in filename
            or "/" in filename
            or "\\" in filename
        ):
            logger.error(f"Invalid filename: {filename}")
            print(f"Error: Invalid filename: {filename}")
            return None

        # Extract the file extension
        extension = Path(filename).suffix.lower()
        logger.info(f"Creating file: {filename}")

        # Get today's date in YYYY-MM-DD format
        today = datetime.date.today().strftime("%Y-%m-%d")

        # Get the language based on the extension
        supported_extensions = utils.get_supported_languages()
        language = supported_extensions.get(extension, "")

        # Check if the extension is supported
        if not language:
            logger.error(f"Unsupported file extension: {extension}")
            print(f"Error: Unsupported file extension: {extension}")
            print(f"Supported extensions: {', '.join(supported_extensions.keys())}")
            return None

        # Construct paths for the playground and today's folder
        playground_folder = Path(config.base_dir) / f"{language}-playground"
        today_folder = playground_folder / today
        logger.debug(f"Using directory: {today_folder}")

        # Create the directories if they do not exist
        today_folder.mkdir(parents=True, exist_ok=True)

        # Construct the full file path
        file_path = today_folder / filename

        # Generate content from template
        file_content = get_file_template(language, filename, str(today_folder))

        # Create the file if it does not exist, or if forced
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(file_content)
            logger.info(f"Created file: {file_path}")
            print(f"Created file: {file_path}")
        else:
            logger.warning(f"File already exists: {file_path}")
            print(f"File already exists: {file_path}")

        return str(file_path)

    except OSError as e:
        logger.error(f"Error creating directories: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

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
        logger.warning("No editor command configured. Skipping editor launch.")
        print("No editor command configured. Skipping editor launch.")
        return False

    # Validate path does not contain shell injection chars when formatted
    try:
        # If editor_command contains {path}, replace with quoted path and split
        if "{path}" in editor_cmd:
            # Split command safely: format then shlex.split, no shell
            cmd_str = editor_cmd.format(path=path)
            # Use shlex.split without shell; pass as list
            cmd_parts = shlex.split(cmd_str)
        else:
            cmd_parts = shlex.split(editor_cmd) + [path]

        subprocess.run(cmd_parts, shell=False, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to open editor. Command '{editor_cmd}' returned non-zero exit status {e.returncode}"
        )
        print(
            f"Failed to open editor. Command '{editor_cmd}' returned non-zero exit status {e.returncode}"
        )
        return False
    except Exception as e:
        logger.error(f"Error opening editor: {e}")
        print(f"Error opening editor: {e}")
        return False


def main() -> int:
    """
    Main function to handle command line arguments and execute program logic.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    logger.info("Starting CodePG")

    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="CodePG - A CLI application to automate coding playground setup"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create file command (default behavior)
    create_parser = subparsers.add_parser("create", help="Create a new file (default command)")
    create_parser.add_argument(
        "filename", type=str, help="The name of the file to be created (including extension)."
    )
    create_parser.add_argument("--config", "-c", type=str, help="Path to the configuration file.")
    create_parser.add_argument(
        "--no-editor", action="store_true", help="Don't open the editor after creating the file."
    )

    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument(
        "--init", action="store_true", help="Create a default configuration file"
    )
    config_parser.add_argument(
        "--set", nargs=2, metavar=("KEY", "VALUE"), help="Set a configuration option"
    )
    config_parser.add_argument("--show", action="store_true", help="Show the current configuration")
    config_parser.add_argument("--file", type=str, help="Specify a configuration file location")
    config_parser.add_argument(
        "--edit", action="store_true", help="Open the configuration file in your default editor"
    )

    # For backward compatibility: if no subcommand is provided but a filename is, use 'create'
    args, unknown = parser.parse_known_args()
    if not args.command and unknown and not unknown[0].startswith("-"):
        args.command = "create"
        args.filename = unknown[0]
        args.config = None
        args.no_editor = False

        if len(unknown) > 1:
            for i, arg in enumerate(unknown[1:], 1):
                if arg == "--no-editor":
                    args.no_editor = True
                elif arg == "--config" or arg == "-c":
                    if i + 1 < len(unknown):
                        args.config = unknown[i + 1]

    # If no command was provided explicitly or implicitly, show help
    if not args.command:
        parser.print_help()
        return 0

    # Handle config management command
    if args.command == "config":
        logger.info("Handling configuration command")
        return handle_config_command(args)

    # Handle file creation (the default command)
    if args.command == "create":
        logger.info(f"Creating file: {args.filename}")
        # Load configuration
        try:
            config = Config(config_path=args.config)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
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
                logger.warning("Failed to open editor but file was created successfully.")
                print("Warning: Failed to open editor but file was created successfully.")

    return 0


def handle_config_command(args: Any) -> int:
    """
    Handle configuration management commands.

    Parameters:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    config_file = args.file

    if args.init:
        # Create default config file
        success, message = Config.create_default_config(Path(config_file) if config_file else None)
        if success:
            logger.info(f"Created default configuration file at: {message}")
            print(f"Created default configuration file at: {message}")
            if args.edit:
                # Try to open the config file in editor
                editor_cmd = utils.detect_default_editor() or 'code "{path}"'
                open_file_in_editor(message, editor_cmd)
            return 0
        else:
            logger.error(f"Failed to create default configuration: {message}")
            print(f"Failed to create default configuration: {message}")
            return 1

    # Load existing configuration
    try:
        config = Config(config_path=config_file)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        print(f"Error loading configuration: {e}")
        return 1

    # Set a configuration option
    if args.set:
        key, value = args.set
        if config.set(key, value):
            success, message = config.save()
            if success:
                logger.info(f"Set {key}={value} in {message}")
                print(f"Set {key}={value} in {message}")
                return 0
            else:
                logger.error(f"Failed to save configuration: {message}")
                print(f"Failed to save configuration: {message}")
                return 1
        else:
            logger.error(f"Unknown configuration option: {key}")
            print(f"Unknown configuration option: {key}")
            return 1

    # Show the current configuration
    if args.show:
        config_data = config.show_all()
        logger.info("Current configuration:")
        print("Current configuration:")
        for key, value in config_data.items():
            print(f"  {key}: {value}")
        print(f"\nLoaded from: {config.loaded_from or 'Default values'}")
        print("\nYou can set these values using:")
        print("  codepg config --set KEY VALUE")
        print("Or with environment variables:")
        for key in config_data:
            print(f"  export CODEPG_{key.upper()}=value")
        return 0

    # Edit the configuration file
    if args.edit:
        if not config.loaded_from:
            logger.warning("No configuration file exists yet. Use --init to create one.")
            print("No configuration file exists yet. Use --init to create one.")
            return 1

        # Try to open the config file in editor
        editor_cmd = utils.detect_default_editor() or 'code "{path}"'
        return 0 if open_file_in_editor(str(config.loaded_from), editor_cmd) else 1

    # If no specific config action is requested, show help
    logger.warning(
        "No configuration action specified. Use one of --init, --set, --show, or --edit."
    )
    print("No configuration action specified. Use one of --init, --set, --show, or --edit.")
    return 1


def open_file_in_editor(file_path: str, editor_cmd: str) -> bool:
    """
    Open a file in the specified editor.

    Parameters:
        file_path (str): Path to the file to open.
        editor_cmd (str): Command template to use for opening.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        if "{path}" in editor_cmd:
            cmd_str = editor_cmd.format(path=file_path)
            cmd_parts = shlex.split(cmd_str)
        else:
            cmd_parts = shlex.split(editor_cmd) + [file_path]
        subprocess.run(cmd_parts, shell=False, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to open editor. Command '{editor_cmd}' returned non-zero exit status {e.returncode}"
        )
        print(
            f"Failed to open editor. Command '{editor_cmd}' returned non-zero exit status {e.returncode}"
        )
        return False
    except Exception as e:
        logger.error(f"Error opening editor: {e}")
        print(f"Error opening editor: {e}")
        return False


if __name__ == "__main__":
    sys.exit(main())
