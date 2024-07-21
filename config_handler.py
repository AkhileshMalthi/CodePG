import json

# Path to the configuration file (replace with your desired location)
CONFIG_FILE = 'config.json'

def load_config():
  """
  Loads configuration settings from the JSON file.
  Returns:
      A dictionary containing configuration settings or None if file not found.
  """
  try:
    with open(CONFIG_FILE, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    print(f"Configuration file '{CONFIG_FILE}' not found. Using default base directory.")
    return None

def get_base_dir():
  """
  Retrieves the base directory from the configuration or returns the default.
  Args:
      config: A dictionary containing configuration settings.
  Returns:
      The base directory from the configuration or the default base directory.
  """

  config = load_config()
  
  return config.get('BASE_DIR')
