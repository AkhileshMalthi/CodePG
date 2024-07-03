# CodePG

CodePG is a command-line interface (CLI) application designed to automate the setup of coding playgrounds for various programming languages. It simplifies the process of creating and managing files in dedicated folders, along with opening them in a code editor for immediate use.

## Features

- **File Creation**: Create new files for supported programming languages in date-specific folders.
- **Supported Languages**: Python, JavaScript, Java, C#, C++.
- **Visual Studio Code Integration**: Automatically open the created file in Visual Studio Code for editing.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/CodePG.git
   cd CodePG
   ```

2. **Setup Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   . venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Base Directory**:
   - Open `app.py` and modify `BASE_DIR` to specify the base directory where playground folders will be created.

## Usage

### View Help
```bash
python app.py
```

### Create a New File
```bash
python app.py python --file
```
This command prompts for a filename and creates a Python file (`filename.py`) in today's date folder under `python-playground`. It then opens Visual Studio Code with the folder.

Replace `python` with other supported languages like `javascript`, `java`, `csharp`, or `cpp`.

## Command Line Arguments

- **Positional Argument**:
  - `language`: The programming language (e.g., python, javascript).

- **Optional Flags**:
  - `--file`: Creates a new file for the specified language.

## Support

For any issues or suggestions, please [open an issue](https://github.com/your-username/CodePG/issues).
