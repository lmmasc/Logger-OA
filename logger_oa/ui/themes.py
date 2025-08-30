from __future__ import annotations

from typing import Literal

Theme = Literal["Light", "Dark"]


class ThemeManager:
    def get_qss(self, theme: Theme, font_size: int) -> str:
        base_bg = "#fff" if theme == "Light" else "#232629"
        base_fg = "#232629" if theme == "Light" else "#f0f0f0"
        border = "#bbb" if theme == "Light" else "#444"
        menu_bg = "#f3f3f3" if theme == "Light" else "#23272e"
        accent = "#a63c3c"
        return f"""
QMainWindow, QWidget {{
    background: {base_bg};
    color: {base_fg};
    font-size: {font_size}px;
}}
QMenuBar {{
    background: {menu_bg};
    color: {base_fg};
}}
QPushButton {{
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px 10px;
}}
QPushButton:hover {{
    background: {accent};
    color: #fff;
}}
"""
