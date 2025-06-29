# CodePG - Code PlayGround

A simple, fast command-line tool that helps organize your coding practice by creating date-organized folders and files for various programming languages.

## ✨ Features

- 🗂️ **Organized Structure**: Creates language-specific folders organized by date
- ⚡ **Quick Setup**: One command to create and open files
- 🧠 **AI-Powered**: Generate code snippets using AI (Groq, Ollama)
- 🔧 **Configurable**: Customize editor, directories, and AI settings
- 🌍 **Cross-Platform**: Works on Windows, macOS, and Linux
- 📝 **20+ Languages**: Support for Python, JavaScript, TypeScript, Rust, Go, and more

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/CodePG.git
cd CodePG

# Install with poetry (recommended)
poetry install
poetry shell

# Or install with pip
pip install -e .
```

### Basic Usage

```bash
# Create a Python file
codepg create hello.py

# Create with AI-generated content
codepg create server.py --prompt "Create a simple HTTP server"

# View configuration
codepg config --show

# Set your preferred editor
codepg config --set editor_command "code \"{path}\""
```

## 📖 Usage Examples

### Creating Files

```bash
# Basic file creation
codepg create calculator.py
codepg create app.js
codepg create main.rs

# Skip opening editor
codepg create test.py --no-editor

# Generate code with AI
codepg create fibonacci.py --prompt "Create a function to calculate fibonacci numbers"
```

### Configuration Management

```bash
# Initialize default config
codepg config --init

# Show current settings
codepg config --show

# Customize settings
codepg config --set base_dir "D:/MyCodePlaygrounds"
codepg config --set editor_command "nvim \"{path}\""

# Edit config file directly
codepg config --edit
```

### AI Code Generation

Set up your API key:
```bash
# For Groq (default)
export GROQ_API_KEY="your-groq-api-key"

# Configure AI settings
codepg config --set ai_model_type groq
codepg config --set ai_model_name "mixtral-8x7b-32768"
```

## ⚙️ Configuration

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
| `ai_model_type` | AI provider (`groq` or `ollama`) | `groq` |
| `ai_model_name` | Specific model name | `null` (uses default) |

### Environment Variables

Override any setting with environment variables:
```bash
export CODEPG_BASE_DIR="/path/to/playgrounds"
export CODEPG_EDITOR_COMMAND="vim \"{path}\""
export CODEPG_AI_MODEL_TYPE="ollama"
```

## 🔧 Supported Languages

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

## 📁 Directory Structure

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

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/yourusername/CodePG.git
cd CodePG
poetry install
poetry shell

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Check code quality
ruff check codepg/
ruff format codepg/
mypy codepg/
```

### Project Structure

```
codepg/
├── __init__.py
├── app.py          # Main CLI application
├── config.py       # Configuration management
├── utils.py        # Utility functions
├── logger.py       # Logging setup
└── ai/
    ├── __init__.py
    ├── base_ai.py   # AI interface
    ├── groq_ai.py   # Groq integration
    └── ollama_ai.py # Ollama integration
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and modern tooling
- AI integration powered by Groq and Ollama
- Code quality ensured by Ruff and MyPy
