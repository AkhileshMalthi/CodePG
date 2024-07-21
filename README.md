# CodePG

CodePG is a command-line interface (CLI) application designed to automate the setup of coding playgrounds for various programming languages. It simplifies the process of creating and managing files in dedicated folders, along with opening them in a code editor for immediate use.

## Features

- **File Creation**: Create new files for supported programming languages in date-specific folders.
- **Supported Languages**: Python, JavaScript, Java, C#, C++.
- **Visual Studio Code Integration**: Automatically open the created file in Visual Studio Code for editing.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AkhileshMalthi/CodePG.git
   cd CodePG
   ```

2. **Setup Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   . venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Set Some Configurations**:
   - Open `app.py` and modify `BASE_DIR` to specify the base directory where playground folders will be created.
   - Provide the `app.py` path in `codepg.bat` file and Add `codepg.bat` to `PATH`

## Usage

### View Help
```bash
codepg --help
```

### Create a New File
```bash
codepg filename.py
```
This command creates the `filename.py` in the DD-MM-YYYY ( The date it was created) folder in the python-playground directory ( which is got by the extension of the filename ).
 It then opens Visual Studio Code with the folder.

## Support

For any issues or suggestions, please [open an issue](https://github.com/AkhileshMalthi/CodePG/issues).
