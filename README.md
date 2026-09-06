# CodePG - Code Playground

CodePG is a command-line tool (CLI) that creates date-organized playground files so you can practice any language without manual folder setup.

You run one command and get a file with a starter template (code snippet inserted at creation) in `~/CodePG/<language>-playground/YYYY-MM-DD/`. Use it when you want to try a language, test an idea, or keep daily practice separated by date.

## How it works

```
you type:  codepg create hello.py  (or: codepg hello.py)
                |
                v
      +--------------------+
      | parse filename     |  read extension -> language (utils.py:22)
      |  hello.py -> python|
      +--------+-----------+
               |
      +--------------------+
      | build paths        |  base_dir + language + today
      | ~/CodePG/python-   |  ex: ~/CodePG/python-playground/2026-09-06/hello.py
      | playground/YYYY-MM-DD|
      +--------+-----------+
               |
      +--------------------+
      | write template     |  language-specific starter (app.py:23)
      |  or fallback       |
      +--------+-----------+
               |
      +--------------------+
      | open in editor     |  runs editor_command with the day folder (app.py:146)
      |  code "{path}"     |  skip with --no-editor
      +--------------------+
```

## Features

| Feature | What it does |
|---|---|
| Date-organized playgrounds | Creates `~/CodePG/<language>-playground/YYYY-MM-DD/<file>` on every run |
| One-command creation | `codepg create <file>` or shorthand `codepg <file>` |
| One-command sandboxes | `codepg sandbox <language> [name]` spins up a full project (native init) for learning |
| Starter templates | Built-in templates for 20 languages (see table below); unknown extensions get a fallback comment |
| Editor integration | Opens the day folder (or sandbox folder) in your editor after creation; configure any command |
| Config cascade | CLI flag, env var, then config file (see Configuration) |
| Cross-platform | Works on Windows, macOS, Linux; detects `code`, `notepad`, `nano`, `vim` etc. |
| Docker and dev container | Run without local Python via `Dockerfile` or VS Code Dev Container |

## Requirements

- Python 3.11 to 3.13
- [uv](https://docs.astral.sh/uv/) for install and run (recommended)

## Quick start

```bash
# 1. Clone
git clone https://github.com/AkhileshMalthi/CodePG.git
cd CodePG

# 2. Install dependencies
uv sync --group dev

# 3. Check it works
uv run codepg --help

# 4. Create your first file (also opens in editor)
uv run codepg create hello.py

# 5. Create without opening editor
uv run codepg create hello.py --no-editor
```

Alternative install without uv:

```bash
pip install -e .
codepg create hello.py
```

Docker:

```bash
docker build -t codepg .
docker run --rm -v "$HOME/CodePG:/playgrounds" codepg create hello.py --no-editor
docker run --rm codepg --help
```

Dev container (VS Code): open the folder and choose "Reopen in Container". The container installs `uv` and runs `uv sync --group dev` for you.

## Usage

### Create files

```bash
# Shorthand also works (no "create" word)
uv run codepg hello.py
uv run codepg create calculator.py
uv run codepg create app.js
uv run codepg create main.rs
uv run codepg create Main.java        # class name is sanitized to valid Java

# Use a different config file for one run
uv run codepg create hello.py --config /path/to/config.json

# List what you created (example)
ls ~/CodePG/python-playground/2026-09-06/
```

If the file already exists, CodePG keeps the existing file and does not overwrite it.

If the extension is not supported, CodePG prints the list of supported extensions and exits with code 1.

### Create sandboxes

```bash
# Spin up a full project sandbox for a language (uses native init tools)
uv run codepg sandbox python                  # random name: sandbox-py-a3f9
uv run codepg sandbox python my-algos         # custom name
uv run codepg sandbox python my-algos --git   # also run git init
uv run codepg sandbox python --no-editor      # skip opening editor
uv run codepg sandbox --list                  # list supported languages (python, javascript, typescript, go, rust, java)

# Aliases work too: py, js, ts, rs, golang
uv run codepg sandbox js my-js-lab
uv run codepg sandbox --help
```

Sandboxes are created in `~/CodePG/<language>-playground/YYYY-MM-DD/<sandbox-name>/`.

| Language | Native init (tried first) | Fallback if tool missing |
|---|---|---|
| `python` | `uv init --name <name> --bare` | `main.py` + `pyproject.toml` + `README.md` |
| `javascript` | `npm init -y` | `index.js` + `package.json` + `README.md` |
| `typescript` | `npm init -y` + `tsconfig.json` | `index.ts` + `package.json` + `tsconfig.json` |
| `go` | `go mod init <name>` | `main.go` + `go.mod` + `README.md` |
| `rust` | `cargo init --name <name> --bin --vcs none` | `main.rs` + `Cargo.toml` + `README.md` |
| `java` | (no native init) | `<Class>.java` + `README.md` |

If the native tool is not installed, CodePG falls back to a minimal scaffold so the command always succeeds. If the sandbox folder already exists and is non-empty, it is kept and not overwritten (same as single-file `create`).

### Manage configuration

```bash
# Create a default config file at ./codepg_config.json
uv run codepg config --init

# Create at a custom path
uv run codepg config --init --file /path/to/my.json

# Show current config and where it was loaded from
uv run codepg config --show

# Change a value
uv run codepg config --set base_dir "D:/MyCodePlaygrounds"
uv run codepg config --set editor_command "nvim \"{path}\""

# Open the config file in your editor
uv run codepg config --edit
```

## Configuration

CodePG resolves config in this order (first match wins):

| Priority | Source | Example |
|---|---|---|
| 1 | `--config` flag | `codepg create hello.py --config ./my.json` |
| 2 | Env var `CODEPG_CONFIG_FILE` | `CODEPG_CONFIG_FILE=./my.json codepg create hello.py` |
| 3 | `./codepg_config.json` | Current directory |
| 4 | `~/.config/codepg/config.json` | User config dir |
| 5 | `~/.codepg.json` | Home fallback |
| 6 | Built-in defaults | See table below |

| Option | Env var | Default | Notes |
|---|---|---|---|
| `base_dir` | `CODEPG_BASE_DIR` | `~/CodePG` | Root for all playgrounds |
| `editor_command` | `CODEPG_EDITOR_COMMAND` | `code "{path}"` | Must contain `{path}` placeholder; runs without shell |

`{path}` is replaced with the day folder (e.g. `~/CodePG/python-playground/2026-09-06`). The command is split with `shlex.split` (safe tokenization) and run without shell.

## Supported languages

| Extension | Language | Extension | Language |
|---|---|---|---|
| `.py` | Python | `.go` | Go |
| `.js` | JavaScript | `.rs` | Rust |
| `.ts` | TypeScript | `.java` | Java |
| `.html` | HTML | `.cs` | C# |
| `.css` | CSS | `.php` | PHP |
| `.c` | C | `.rb` | Ruby |
| `.cpp` | C++ | `.swift` | Swift |
| `.h` | C Header | `.kt` | Kotlin |
| `.hpp` | C++ Header | `.sql` | SQL |
| `.sh` | Shell | `.dart` | Dart |
| `.lua` | Lua | `.r` | R |

Templates exist for each language above. The Java template sanitizes the filename into a valid class name.

## Directory structure

```
~/CodePG/
├── python-playground/
│   ├── 2026-09-06/
│   │   ├── hello.py
│   │   ├── calculator.py
│   │   ├── my-algos/              # sandbox: uv init
│   │   │   ├── pyproject.toml
│   │   │   ├── main.py
│   │   │   └── README.md
│   │   └── sandbox-py-a3f9/       # auto-named sandbox
│   │       ├── pyproject.toml
│   │       └── main.py
│   └── 2026-09-07/
│       └── parser.py
├── javascript-playground/
│   └── 2026-09-06/
│       └── app.js
└── rust-playground/
    └── 2026-09-06/
        ├── main.rs
        └── my-rs-lab/             # sandbox: cargo init
            ├── Cargo.toml
            └── src/main.rs
```

## Development

```bash
git clone https://github.com/AkhileshMalthi/CodePG.git
cd CodePG
uv sync --group dev
uv run pre-commit install

# Run all checks
uv run ruff check codepg/ tests/
uv run ruff format codepg/ tests/
uv run mypy codepg/
uv run pytest

# Shortcuts
uv run python scripts/dev.py all
make all
```

Project layout:

```
codepg/
├── __init__.py       # version from importlib.metadata (import system that reads package version)
├── app.py            # CLI, file creation, sandbox routing, editor launch
├── sandbox.py        # sandbox creation (native init + fallback)
├── config.py         # config load/save and env overrides
├── utils.py          # language map, sandbox language map, editor detection
└── logger.py         # colored log formatter
tests/
├── conftest.py
├── test_cli.py
├── test_config.py
├── test_file_creation.py
└── test_utils.py
```

Tooling: `uv` for package management, `ruff` for lint and format (code style tool), `mypy` for type checking (checks type annotations), `pytest` for tests, `pre-commit` for git hooks (scripts that run before commit).

## Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: your change"`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

## Releases

CodePG uses Semantic Versioning (number system `MAJOR.MINOR.PATCH`) and Conventional Commits (commit format `type: description`).

| Commit type | Version bump | Example |
|---|---|---|
| `fix: ...` | PATCH | `fix: handle slash in filename` -> `0.1.0` -> `0.1.1` |
| `feat: ...` | MINOR | `feat: add lua template` -> `0.1.0` -> `0.2.0` |
| `feat!:` or `BREAKING CHANGE:` | MAJOR | `feat!: change config format` -> `1.0.0` -> `2.0.0` |
| `docs:`, `chore:`, `refactor:` | No release | No version change |

Flow:

1. You open a PR with `feat:`/`fix:` commits and merge to `main`.
2. GitHub Actions runs `release.yml` on `main`, bumps `pyproject.toml:3` and `codepg/__init__.py:3`, updates `CHANGELOG.md`, creates tag `vX.Y.Z`, and publishes a GitHub Release with `dist/*` files (built via `uv build`).
3. No manual `cz bump` (manual version bump) — CI does it. If you push only `docs:`/`chore:`, no release is made.

Check the next version without releasing: `uv run semantic-release version --print`.

## License

MIT — see [LICENSE](LICENSE).
