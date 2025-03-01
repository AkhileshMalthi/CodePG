# CodePG - Code Playground Generator

CodePG is a command-line tool that helps you organize and automate your coding practice by creating date-organized folders and files for various programming languages.

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

```bash
# Create a Python file
codepg hello.py

# Create a JavaScript file with a custom config
codepg script.js --config ./my_config.json

# Create a file without opening an editor
codepg test.py --no-editor
```

## Configuration

CodePG looks for configuration in the following locations (in order):

1. Path specified with --config argument
2. ./codepg_config.json (in the current directory)
3. ~/.config/codepg/config.json
4. ~/.codepg.json

Example configuration:

```json
{
    "base_dir": "D:/CodePlaygrounds",
    "editor_command": "code \"{path}\""
}
```

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
