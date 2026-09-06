"""CodePG - A CLI application to automate coding playground setup."""

from importlib.metadata import version as _get_version

try:
    __version__ = _get_version("codepg")
except Exception:
    __version__ = "0.1.0"
