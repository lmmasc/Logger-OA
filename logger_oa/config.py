from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Literal, Tuple

from .utils.paths import get_user_config_dir

Theme = Literal["Light", "Dark"]


@dataclass
class AppConfig:
    theme: Theme = "Light"
    font_size: int = 18

    @staticmethod
    def _config_file() -> str:
        cfg_dir = get_user_config_dir()
        os.makedirs(cfg_dir, exist_ok=True)
        return os.path.join(cfg_dir, "config.json")

    @classmethod
    def load(cls) -> "AppConfig":
        path = cls._config_file()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Migrate Spanish theme names if present
                theme = data.get("theme", "Light")
                if theme in ("Claro", "Oscuro"):
                    theme = "Light" if theme == "Claro" else "Dark"
                font_size = int(data.get("font_size", 18))
                return cls(theme=theme, font_size=font_size)
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        path = self._config_file()
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"theme": self.theme, "font_size": self.font_size}, f)


__all__ = ["AppConfig", "Theme"]
