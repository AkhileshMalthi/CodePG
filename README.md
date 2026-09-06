# CodePG - Code PlayGround

A simple, fast command-line tool (CLI) that helps organize your coding practice by creating date-organized folders and files for various programming languages.

## Features

- **Organized Structure**: Creates language-specific folders organized by date
- **Quick Setup**: One command to create and open files
- **Configurable**: Customize editor and directories
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **20+ Languages**: Support for Python, JavaScript, TypeScript, Rust, Go, and more
- **Docker Ready**: Run via Docker or Dev Container

## Quick Start

### Installation with uv (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/CodePG.git
cd CodePG

# Install uv if you don't have it: https://docs.astral.sh/uv/getting-started/installation/
# Then sync dependencies
uv sync --group dev

# Run any command with uv run
uv run codepg --help
```

### Installation with pip

```bash
pip install -e .
```

### Docker

```bash
# Build and run
docker build -t codepg .
docker run --rm -v "$HOME/CodePG:/playgrounds" codepg create hello.py --no-editor
# Or use the image interactively
docker run -it --rm codepg --help
```

### Basic Usage

```bash
# Create a Python file
uv run codepg create hello.py

# View configuration
uv run codepg config --show

# Set your preferred editor
uv run codepg config --set editor_command "code \"{path}\""
```

## Usage Examples

### Creating Files

```bash
# Basic file creation
uv run codepg create calculator.py
uv run codepg create app.js
uv run codepg create main.rs

# Skip opening editor
uv run codepg create test.py --no-editor

# With custom config
uv run codepg create hello.py --config /path/to/config.json
```

### Configuration Management

```bash
# Initialize default config
uv run codepg config --init

# Show current settings
uv run codepg config --show

# Customize settings
uv run codepg config --set base_dir "D:/MyCodePlaygrounds"
uv run codepg config --set editor_command "nvim \"{path}\""

# Edit config file directly
uv run codepg config --edit
```

## Configuration

CodePG looks for configuration in this order:
1. `--config` argument path
2. `CODEPG_CONFIG_FILE` environment variable
3. `./codepg_config.json` (current directory)
4. `~/.config/codepg/config.json`
5. `~/.codepg.json`

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `base_dir` | Base directory for playgrounds | `~/CodePG` |
| `editor_command` | Command to open editor | `code "{path}"` |

### Environment Variables

Override any setting with environment variables:
```bash
export CODEPG_BASE_DIR="/path/to/playgrounds"
export CODEPG_EDITOR_COMMAND="vim \"{path}\""
```

## Supported Languages

| Extension | Language | Extension | Language |
|-----------|----------|-----------|----------|
| `.py` | Python | `.go` | Go |
| `.js` | JavaScript | `.rs` | Rust |
| `.ts` | TypeScript | `.java` | Java |
| `.html` | HTML | `.cs` | C# |
| `.css` | CSS | `.php` | PHP |
| `.c` | C | `.rb` | Ruby |
| `.cpp` | C++ | `.swift` | Swift |
| `.sh` | Shell | `.kt` | Kotlin |
| `.sql` | SQL | `.dart` | Dart |
| `.h` | C Header | `.lua` | Lua |
| `.hpp` | C++ Header | `.r` | R |

## Directory Structure

CodePG organizes your files like this:
```
~/CodePG/
├── python-playground/
│   ├── 2025-06-29/
│   │   ├── hello.py
│   │   └── calculator.py
│   └── 2025-06-30/
│       └── web_server.py
├── javascript-playground/
│   └── 2025-06-29/
│       └── app.js
└── rust-playground/
    └── 2025-06-29/
        └── main.rs
```

## Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/yourusername/CodePG.git
cd CodePG
uv sync --group dev

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Check code quality
uv run ruff check codepg/ tests/
uv run ruff format codepg/ tests/
uv run mypy codepg/

# Or use the task runner
uv run python scripts/dev.py all
make all
```

### Dev Container (VS Code)

Open the folder in VS Code and choose "Reopen in Container" when prompted. The container installs `uv` and syncs deps automatically.

### Project Structure

```
codepg/
├── __init__.py       # Version (from importlib.metadata)
├── app.py            # Main CLI application
├── config.py         # Configuration management
├── utils.py          # Utility functions
└── logger.py         # Logging setup
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and modern tooling (uv, Ruff, MyPy)
- Code quality ensured by Ruff and MyPy
