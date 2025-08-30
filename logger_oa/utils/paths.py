from __future__ import annotations

import os
import platform
from typing import Tuple


def get_user_base_dir() -> str:
    if platform.system() == "Windows":
        return os.environ.get("APPDATA", os.path.expanduser("~"))
    return os.path.join(os.path.expanduser("~"), ".config")


def get_user_app_dir() -> str:
    return os.path.join(get_user_base_dir(), "LoggerOA")


def get_user_config_dir() -> str:
    return get_user_app_dir()


def get_database_path() -> str:
    app_dir = get_user_app_dir()
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, "db.sqlite")


def get_operations_dir() -> str:
    """Directory to store Operation JSON files."""
    d = os.path.join(get_user_app_dir(), "operations")
    os.makedirs(d, exist_ok=True)
    return d


def get_contests_dir() -> str:
    """Directory to store Contest JSON files."""
    d = os.path.join(get_user_app_dir(), "contests")
    os.makedirs(d, exist_ok=True)
    return d


__all__ = [
    "get_user_base_dir",
    "get_user_app_dir",
    "get_user_config_dir",
    "get_database_path",
    "get_operations_dir",
    "get_contests_dir",
]
