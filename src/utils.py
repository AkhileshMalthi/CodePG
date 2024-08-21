import os
import configparser  # Assuming you're using INI format

def get_base_dir():
  """
  Reads the base directory from the configuration file or prompts the user.
  Ensures the base directory exists and creates it if necessary.

  Returns:
      str: The base directory path.
  """
  config_file = "config.ini"
  config = configparser.ConfigParser()

  # Check for configuration file
  if not os.path.exists(config_file):
    print(f"Configuration file {config_file} not found. Setting up base directory...")

  # Read config or create a new one if not found
  config.read(config_file)

  # Check if base_dir is set in the DEFAULT section
  base_dir = config.get("DEFAULT", "base_dir", fallback=None)

  if not base_dir:
    # Prompt user for base directory
    base_dir = input("Enter the base directory for CodePG playgrounds: ")
    # if not config.has_section("DEFAULT"):
    #   config.add_section("DEFAULT")
    config.set("DEFAULT", "base_dir", base_dir)
    with open(config_file, "w") as f:
      config.write(f)

  # Ensure the base directory exists (prevent potential security issues)
  if not os.path.exists(base_dir):
    try:
      os.makedirs(base_dir)
      print(f"Created base directory: {base_dir}")
    except OSError as e:
      print(f"Error creating base directory: {e}")
      exit(1)

  # Return the base directory
  return base_dir

def get_supported_languages():
  return {
      '.py': 'python',
      '.js': 'javascript',
      '.java': 'java',
      '.cs': 'csharp',
      '.cpp': 'cpp',
      '.rb': 'ruby',
      '.go': 'go',
      '.rs': 'rust',
      '.kt': 'kotlin',
      '.swift': 'swift',
      '.ts': 'typescript',
      '.html': 'html',
      '.css': 'css',
      '.php': 'php',
      '.sh': 'shell',
      '.pl': 'perl',
      '.r': 'r',
      '.scala': 'scala',
      '.lua': 'lua',
      '.dart': 'dart',
      '.hs': 'haskell',
      '.ex': 'elixir',
      '.clj': 'clojure',
      '.groovy': 'groovy',
      '.m': 'matlab',
      '.ps1': 'powershell',
      '.vbs': 'vbscript'
    }