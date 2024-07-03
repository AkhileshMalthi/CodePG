import argparse
import os
import datetime
import subprocess

# Base directory where all the playground folders will be created
BASE_DIR = 'D:\\MyAppsData\\codepg'  # Change this to your actual directory

# Ensure the base directory exists
try:
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
except OSError as e:
    print(f"Error creating base directory {BASE_DIR}: {e}")
    exit(1)

def create_file(language: str, filename: str) -> None:
    """
    Create a new file for the specified programming language in a date-specific folder.
    
    Parameters:
    language (str): The programming language (e.g., 'python', 'javascript').
    filename (str): The name of the file to be created (without extension).
    """
    try:
        # Get today's date in YYYY-MM-DD format
        today = datetime.date.today().strftime("%Y-%m-%d")
        
        # Construct paths for the playground and today's folder
        playground_folder = os.path.join(BASE_DIR, f"{language}-playground")
        today_folder = os.path.join(playground_folder, today)
        
        # Create the directories if they do not exist
        os.makedirs(today_folder, exist_ok=True)

        # Define file extensions for supported languages
        extension = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'csharp': '.cs',
            'cpp': '.cpp'
        }.get(language, '')

        # Check if the language is supported
        if not extension:
            print(f"Unsupported language: {language}")
            return

        # Construct the full file path
        file_path = os.path.join(today_folder, f"{filename}{extension}")

        # Create the file if it does not exist, and write a comment inside it
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(f"# {filename}{extension} created in {today_folder}\n")
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

        # Command to open Visual Studio Code in the playground folder
        vscode_command = f'code "{today_folder}"'
        try:
            # Run the command to open Visual Studio Code
            subprocess.run(vscode_command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Failed to open Visual Studio Code. Make sure it is installed and in PATH.")

    except OSError as e:
        print(f"Error creating directories: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def show_help() -> None:
    """
    Display the help text for the CLI application.
    """
    help_text = """
    CodePG - A CLI application to automate coding playground setup.
    
    Commands:
    codepg                  - View the full description and commands available to the application.
    codepg <language> --file - Prompts for filename and creates a file of that specified language 
                               in a folder named with the date of the day it was created.
                               Opens a code editor with that playground folder.
    
    Supported languages: python, javascript, java, csharp, cpp
    """
    print(help_text)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="CodePG - A CLI application to automate coding playground setup")
    
    # Positional argument for the programming language
    parser.add_argument('language', nargs='?', help='The Programming Language you want to play with. (e.g., python, javascript)')
    
    # Optional flag to create a new file
    parser.add_argument('--file', action='store_true', help='Creates a new file')

    # Parse the command-line arguments
    args = parser.parse_args()

    # If no language is provided, show the help text
    if not args.language:
        show_help()
    else:
        # If the --file flag is set, prompt for the filename and create the file
        if args.file:
            filename = input("Enter the filename (without extension): ")
            create_file(args.language, filename)
        else:
            # Otherwise, show the help text
            show_help()
