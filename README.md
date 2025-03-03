# CodePG - Code PlayGround

CodePG is a command-line tool that helps you organize and automate your coding practice by creating date-organized folders and files for various programming languages.

## Requirements

- Python 3.8.1 or higher

## Features

- Creates organized folders by language and date
- Automatically opens your preferred editor
- Supports multiple programming languages
- Configurable through a JSON configuration file
- Includes language-specific file templates

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/CodePG.git

# Navigate to the directory
cd CodePG

# Install the package
pip install -e .
```

## Usage

### Creating Files

```bash
# Create a Python file
codepg create hello.py

# For backward compatibility, you can omit the 'create' command
codepg hello.py

# Create a JavaScript file with a custom config
codepg create script.js --config ./my_config.json

# Create a file without opening an editor
codepg create test.py --no-editor
```

### Managing Configuration

```bash
# Create a default configuration file
codepg config --init

# Create and immediately open the configuration file in your editor
codepg config --init --edit

# View your current configuration
codepg config --show

# Set a configuration option
codepg config --set base_dir "D:/CodePlaygrounds"
codepg config --set editor_command "sublime \"{path}\""

# Edit your configuration in your default editor
codepg config --edit

# Specify a custom configuration file
codepg config --file "./custom_config.json" --show
```

## Configuration

### Configuration Locations

CodePG looks for configuration in the following locations (in order):

1. Path specified with `--config` argument or `--file` for config commands
2. Path in environment variable `CODEPG_CONFIG_FILE`
3. `./codepg_config.json` (in the current directory)
4. `~/.config/codepg/config.json`
5. `~/.codepg.json`

### Configuration Options

Example configuration:

```json
{
    "base_dir": "D:/CodePlaygrounds",
    "editor_command": "code \"{path}\""
}
```

### Environment Variables

You can also use environment variables to override configuration:

```bash
# Set the base directory for code playgrounds
export CODEPG_BASE_DIR="D:/CodePlaygrounds"

# Set the editor command
export CODEPG_EDITOR_COMMAND="vim \"{path}\""

# Specify a config file to use
export CODEPG_CONFIG_FILE="./my_config.json"
```

## AI Code Generation

CodePG can generate code using AI models based on a prompt:

```bash
# Generate Python code that creates a web server
codepg create server.py --prompt "Create a simple HTTP server that serves files from the current directory"

# Generate JavaScript code for a calculator
codepg create calculator.js --prompt "Build a calculator with basic operations" 
```

### AI Configuration

You can configure AI settings in your config file:

```bash
# Set the AI model to use
codepg config --set ai_model_type groq  # Use Groq API (default)
codepg config --set ai_model_type ollama  # Use local Ollama models

# Set a specific model
codepg config --set ai_model_name llama3-70b-8192  # For Groq
codepg config --set ai_model_name llama3  # For Ollama

# Use CrewAI for more complex tasks
codepg config --set use_crew_ai true
```

### Environment Variables

You can also set up API keys using environment variables:

```bash
# Set up Groq API key
export GROQ_API_KEY="your-api-key-here"
```

Or add it to your `.env` file in the project directory.

## Supported Languages

CodePG currently supports the following file extensions:

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- HTML (.html)
- CSS (.css)
- Go (.go)
- Rust (.rs)
- C (.c, .h)
- C++ (.cpp, .hpp)
- Java (.java)
- C# (.cs)
- PHP (.php)
- Ruby (.rb)
- Shell (.sh)
- And many more!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
