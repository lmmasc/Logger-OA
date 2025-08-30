from __future__ import annotations

"""Minimal application bootstrap (no UI initialization here).

Provides access to configuration and environment paths.
"""

from .config import AppConfig


def load_app_config() -> AppConfig:
    return AppConfig.load()


__all__ = ["load_app_config", "AppConfig"]
