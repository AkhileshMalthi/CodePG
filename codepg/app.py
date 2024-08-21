import argparse
import os
import datetime
import subprocess
import utils

# Base directory where all the playground folders will be created
BASE_DIR = utils.get_base_dir()

SUPPORTED_EXTENSIONS = utils.get_supported_languages()

# Ensure the base directory exists
try:
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
except OSError as e:
    print(f"Error creating base directory {BASE_DIR}: {e}")
    exit(1)


def create_file(filename: str) -> None:
    """
    Create a new file for the specified programming language in a date-specific folder.

    Parameters:
        filename (str): The name of the file to be created (including extension).
    """
    try:
        # Extract the file extension
        extension = os.path.splitext(filename)[1].lower()

        # Get today's date in YYYY-MM-DD format
        today = datetime.date.today().strftime("%Y-%m-%d")

        # Get the language based on the extension
        language = SUPPORTED_EXTENSIONS.get(extension, '')

        # Check if the extension is supported
        if not language:
            print(f"Unsupported file extension: {extension}")
            return

        # Construct paths for the playground and today's folder
        playground_folder = os.path.join(BASE_DIR, f"{language}-playground")
        today_folder = os.path.join(playground_folder, today)

        # Create the directories if they do not exist
        os.makedirs(today_folder, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(today_folder, filename)

        # Create the file if it does not exist, and write a comment inside it
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(f"# {filename} created in {today_folder}\n")
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

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="CodePG - A CLI application to automate coding playground setup")

    # Add argument for filename
    parser.add_argument("filename", type=str, help="The name of the file to be created (including extension).")

    # Parse arguments
    args = parser.parse_args()

    # Call create_file function with the parsed filename
    create_file(args.filename)

if __name__ == "__main__":
  main()
