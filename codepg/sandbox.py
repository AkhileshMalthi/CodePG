"""Sandbox creation using native language init tools with fallback."""

import datetime
import re
import secrets
import subprocess
from pathlib import Path

from codepg import utils
from codepg.config import Config
from codepg.logger import setup_logger

logger = setup_logger(__name__)

# Languages that support sandbox (canonical names)
SANDBOX_LANGUAGES = utils.get_sandbox_languages()


def _sanitize_sandbox_name(name: str) -> str:
    """Sanitize user-provided sandbox name to safe folder name."""
    stem = name.strip()
    sanitized = re.sub(r"[^A-Za-z0-9_-]", "_", stem)
    if not sanitized:
        sanitized = "sandbox"
    if sanitized[0].isdigit():
        sanitized = f"_{sanitized}"
    return sanitized


def generate_default_name(language: str) -> str:
    """Generate a default sandbox name like sandbox-py-a3f9."""
    # short suffix: language abbrev + 4 hex chars
    abbrev_map = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "go": "go",
        "rust": "rs",
        "java": "java",
    }
    abbrev = abbrev_map.get(language, language[:2])
    suffix = secrets.token_hex(2)  # 4 hex chars
    return f"sandbox-{abbrev}-{suffix}"


def _validate_sandbox_name(name: str) -> str | None:
    """Validate sandbox name, return error string or None if valid."""
    if Path(name).name != name or ".." in name or "/" in name or "\\" in name:
        return f"Invalid sandbox name: {name}"
    if not name or not name.strip():
        return "Sandbox name cannot be empty"
    return None


def _run_command(cmd: list[str], cwd: Path) -> bool:
    """Run a command in cwd, return True on success."""
    try:
        result = subprocess.run(cmd, cwd=str(cwd), shell=False, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Command succeeded: {' '.join(cmd)}")
            return True
        logger.warning(
            f"Command failed ({result.returncode}): {' '.join(cmd)} stderr={result.stderr}"
        )
        return False
    except FileNotFoundError:
        logger.warning(f"Command not found: {cmd[0]}")
        return False
    except Exception as e:
        logger.warning(f"Error running {' '.join(cmd)}: {e}")
        return False


def _fallback_scaffold(language: str, sandbox_path: Path, sandbox_name: str) -> None:
    """Create minimal fallback files when native init is unavailable."""
    today = datetime.date.today()
    # Import here to avoid circular import
    from codepg.app import _sanitize_java_class, get_file_template

    # File mapping for fallback
    fallback_files: dict[str, str] = {}

    if language == "python":
        fallback_files["main.py"] = get_file_template("python", "main.py", str(sandbox_path))
        fallback_files["README.md"] = (
            f"# {sandbox_name}\n\nPython sandbox created {today}.\n\nRun with `python main.py`.\n"
        )
        fallback_files[".gitignore"] = "__pycache__/\n*.pyc\n.venv/\n"
        fallback_files["pyproject.toml"] = (
            f'[project]\nname = "{sandbox_name}"\nversion = "0.1.0"\n'
            f'description = "Sandbox {sandbox_name}"\nrequires-python = ">=3.11"\n'
        )
    elif language == "javascript":
        fallback_files["index.js"] = get_file_template("javascript", "index.js", str(sandbox_path))
        fallback_files["README.md"] = (
            f"# {sandbox_name}\n\nJavaScript sandbox created {today}.\n\nRun with `node index.js`.\n"
        )
        fallback_files[".gitignore"] = "node_modules/\n"
        fallback_files["package.json"] = (
            '{\n  "name": "' + sandbox_name + '",\n  "version": "1.0.0",\n'
            '  "main": "index.js",\n  "scripts": {"start": "node index.js"}\n}\n'
        )
    elif language == "typescript":
        fallback_files["index.ts"] = get_file_template("typescript", "index.ts", str(sandbox_path))
        fallback_files["README.md"] = (
            f"# {sandbox_name}\n\nTypeScript sandbox created {today}.\n\nRun with `npx ts-node index.ts`.\n"
        )
        fallback_files[".gitignore"] = "node_modules/\ndist/\n"
        fallback_files["package.json"] = (
            '{\n  "name": "' + sandbox_name + '",\n  "version": "1.0.0",\n'
            '  "main": "index.ts",\n  "scripts": {"start": "ts-node index.ts"}\n}\n'
        )
        fallback_files["tsconfig.json"] = (
            '{\n  "compilerOptions": {\n    "target": "ES2020",\n    "module": "commonjs",\n'
            '    "strict": true,\n    "esModuleInterop": true\n  }\n}\n'
        )
    elif language == "go":
        fallback_files["main.go"] = get_file_template("go", "main.go", str(sandbox_path))
        fallback_files["README.md"] = (
            f"# {sandbox_name}\n\nGo sandbox created {today}.\n\nRun with `go run main.go`.\n"
        )
        fallback_files[".gitignore"] = "bin/\n"
        fallback_files["go.mod"] = f"module {sandbox_name}\n\ngo 1.21\n"
    elif language == "rust":
        fallback_files["main.rs"] = get_file_template("rust", "main.rs", str(sandbox_path))
        # Provide both flat file and src/ layout for compatibility
        fallback_files["README.md"] = (
            f"# {sandbox_name}\n\nRust sandbox created {today}.\n\nRun with `rustc main.rs -o main && ./main` or `cargo run`.\n"
        )
        fallback_files[".gitignore"] = "/target\n"
        fallback_files["Cargo.toml"] = (
            f'[package]\nname = "{sandbox_name}"\nversion = "0.1.0"\nedition = "2021"\n\n'
            f"[dependencies]\n"
        )
    elif language == "java":
        java_class = _sanitize_java_class(sandbox_name)
        fallback_files[f"{java_class}.java"] = get_file_template(
            "java", f"{java_class}.java", str(sandbox_path)
        )
        fallback_files["README.md"] = (
            f"# {sandbox_name}\n\nJava sandbox created {today}.\n\nCompile with `javac {java_class}.java && java {java_class}`.\n"
        )
        fallback_files[".gitignore"] = "*.class\n"

    for rel, content in fallback_files.items():
        dest = sandbox_path / rel
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        logger.info(f"Created fallback file: {dest}")


def _run_native_init(language: str, sandbox_path: Path, sandbox_name: str) -> bool:
    """Attempt native init for language. Return True if native init succeeded."""
    if language == "python":
        # uv init --name <name> --bare creates pyproject.toml without extra files
        # Try bare first, then without --bare, then plain uv init
        for cmd in [
            ["uv", "init", "--name", sandbox_name, "--bare"],
            ["uv", "init", "--name", sandbox_name],
            ["uv", "init", "--bare"],
            ["uv", "init"],
        ]:
            if _run_command(cmd, sandbox_path):
                # Ensure main.py exists (uv --bare does not create it)
                main_py = sandbox_path / "main.py"
                if not main_py.exists():
                    from codepg.app import get_file_template

                    main_py.write_text(
                        get_file_template("python", "main.py", str(sandbox_path)), encoding="utf-8"
                    )
                # Ensure README exists
                readme = sandbox_path / "README.md"
                if not readme.exists():
                    readme.write_text(f"# {sandbox_name}\n\nPython sandbox.\n", encoding="utf-8")
                return True
        return False

    if language == "javascript":
        if _run_command(["npm", "init", "-y"], sandbox_path):
            # Ensure index.js exists
            idx = sandbox_path / "index.js"
            if not idx.exists():
                from codepg.app import get_file_template

                idx.write_text(
                    get_file_template("javascript", "index.js", str(sandbox_path)), encoding="utf-8"
                )
            return True
        return False

    if language == "typescript":
        if _run_command(["npm", "init", "-y"], sandbox_path):
            idx = sandbox_path / "index.ts"
            if not idx.exists():
                from codepg.app import get_file_template

                idx.write_text(
                    get_file_template("typescript", "index.ts", str(sandbox_path)), encoding="utf-8"
                )
            tsconfig = sandbox_path / "tsconfig.json"
            if not tsconfig.exists():
                tsconfig.write_text(
                    '{\n  "compilerOptions": {\n    "target": "ES2020",\n    "module": "commonjs",\n'
                    '    "strict": true,\n    "esModuleInterop": true\n  }\n}\n',
                    encoding="utf-8",
                )
            return True
        return False

    if language == "go":
        # go mod init <name> must run inside sandbox dir
        if _run_command(["go", "mod", "init", sandbox_name], sandbox_path):
            main_go = sandbox_path / "main.go"
            if not main_go.exists():
                from codepg.app import get_file_template

                main_go.write_text(
                    get_file_template("go", "main.go", str(sandbox_path)), encoding="utf-8"
                )
            return True
        return False

    if language == "rust":
        # cargo init --name <name> --bin --vcs none
        # cargo init expects empty dir or will fail; sandbox is empty so OK
        if _run_command(
            ["cargo", "init", "--name", sandbox_name, "--bin", "--vcs", "none"], sandbox_path
        ):
            return True
        # Fallback try without --vcs none if older cargo
        if _run_command(["cargo", "init", "--name", sandbox_name, "--bin"], sandbox_path):
            return True
        return False

    if language == "java":
        # No lightweight native init; use fallback
        return False

    return False


def create_sandbox(
    language_raw: str,
    sandbox_name: str | None,
    config: Config,
    use_git: bool = False,
) -> str | None:
    """
    Create a sandbox for the given language.

    Parameters:
        language_raw (str): User-supplied language name (e.g. 'python', 'js')
        sandbox_name (str | None): Desired sandbox folder name or None for auto.
        config (Config): Config with base_dir.
        use_git (bool): If True, run git init inside sandbox.

    Returns:
        str | None: Path to sandbox dir or None on failure.
    """
    # Validate and normalize language
    canonical = utils.get_language_by_name(language_raw)
    if not canonical:
        print(f"Error: Unsupported language: {language_raw}")
        print(f"Supported languages: {', '.join(sorted(SANDBOX_LANGUAGES.keys()))}")
        print("Tip: use `codepg sandbox --list` to see options")
        return None

    language = canonical

    # Resolve name
    if sandbox_name:
        err = _validate_sandbox_name(sandbox_name)
        if err:
            print(f"Error: {err}")
            return None
        name = _sanitize_sandbox_name(sandbox_name)
    else:
        name = generate_default_name(language)

    # Validate name after sanitizing
    err = _validate_sandbox_name(name)
    if err:
        print(f"Error: {err}")
        return None

    today = datetime.date.today().strftime("%Y-%m-%d")
    playground_folder = Path(config.base_dir) / f"{language}-playground"
    today_folder = playground_folder / today
    sandbox_path = today_folder / name

    # If sandbox already exists and non-empty, do not overwrite
    if sandbox_path.exists() and any(sandbox_path.iterdir()):
        print(f"Sandbox already exists: {sandbox_path}")
        return str(sandbox_path)

    try:
        sandbox_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Creating sandbox: {sandbox_path} for {language}")
    except OSError as e:
        print(f"Error creating sandbox directory: {e}")
        return None

    # Try native init, fallback if fails
    native_ok = _run_native_init(language, sandbox_path, name)
    if not native_ok:
        logger.info(f"Native init unavailable for {language}, using fallback scaffold")
        _fallback_scaffold(language, sandbox_path, name)
    else:
        # Supplement native scaffold with README/.gitignore if missing
        # (native tools like `cargo init` or `go mod init` do not create them)
        today_str = str(datetime.date.today())
        supplements: dict[str, str] = {}
        if language == "go":
            supplements["README.md"] = (
                f"# {name}\n\nGo sandbox created {today_str}.\n\nRun with `go run main.go`.\n"
            )
            supplements[".gitignore"] = "bin/\n"
        elif language == "rust":
            supplements["README.md"] = (
                f"# {name}\n\nRust sandbox created {today_str}.\n\nRun with `cargo run`.\n"
            )
            supplements[".gitignore"] = "/target\n"
        elif language == "javascript":
            supplements["README.md"] = (
                f"# {name}\n\nJavaScript sandbox created {today_str}.\n\nRun with `node index.js`.\n"
            )
            supplements[".gitignore"] = "node_modules/\n"
        elif language == "typescript":
            supplements["README.md"] = (
                f"# {name}\n\nTypeScript sandbox created {today_str}.\n\nRun with `npx ts-node index.ts`.\n"
            )
            supplements[".gitignore"] = "node_modules/\ndist/\n"
        for rel, content in supplements.items():
            dest = sandbox_path / rel
            if not dest.exists():
                dest.write_text(content, encoding="utf-8")
                logger.info(f"Created supplement file: {dest}")

    # Optional git init
    if use_git:
        if utils.is_command_available("git"):
            if _run_command(["git", "init"], sandbox_path):
                print("Initialized git repository")
            else:
                print("Warning: git init failed")
        else:
            print("Warning: git not found, skipping git init")

    print(f"Created sandbox: {sandbox_path}")
    return str(sandbox_path)


def list_sandbox_languages() -> None:
    """Print supported sandbox languages and their init tools."""
    print("Supported sandbox languages:")
    tool_map = {
        "python": "uv init --name <name> --bare",
        "javascript": "npm init -y",
        "typescript": "npm init -y + tsconfig.json",
        "go": "go mod init <name>",
        "rust": "cargo init --name <name> --bin --vcs none",
        "java": "fallback template (no native init)",
    }
    for lang in sorted(SANDBOX_LANGUAGES.keys()):
        tool = tool_map.get(lang, "fallback")
        print(f"  {lang:<12} -> {tool}")
