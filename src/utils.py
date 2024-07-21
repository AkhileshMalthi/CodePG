import os
import configparser  # Assuming you're using INI format

def get_base_dir():
  """
  Reads the base directory from the configuration file or prompts the user.
  """
  config_file = "config.ini"
  config = configparser.ConfigParser()

  # Check for configuration file
  if os.path.exists(config_file):
    config.read(config_file)
    return config.get("DEFAULT", "base_dir")

  # Configuration file doesn't exist or base_dir is missing
  base_dir = input("Enter the base directory for CodePG playgrounds: ")
  with open(config_file, "w") as f:
    config.write(f"[DEFAULT]\nbase_dir = {base_dir}")
  return base_dir

