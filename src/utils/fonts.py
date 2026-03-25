import os

from PySide6.QtGui import QFont, QFontDatabase

from utils.resources import get_resource_path


_ROBOTO_MONO_FAMILY = None


def ensure_roboto_mono_registered() -> str:
    """Registra Roboto Mono (regular/bold) y devuelve la familia disponible."""
    global _ROBOTO_MONO_FAMILY

    if _ROBOTO_MONO_FAMILY:
        return _ROBOTO_MONO_FAMILY

    font_files = [
        "assets/RobotoMono-Regular.ttf",
        "assets/RobotoMono-Bold.ttf",
    ]

    families = []
    for relative_path in font_files:
        font_path = get_resource_path(relative_path)
        if not os.path.exists(font_path):
            continue
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            continue
        families.extend(QFontDatabase.applicationFontFamilies(font_id))

    _ROBOTO_MONO_FAMILY = families[0] if families else "Monospace"
    return _ROBOTO_MONO_FAMILY


def build_roboto_mono_font(point_size: int, bold: bool = False) -> QFont:
    """Construye una QFont basada en Roboto Mono, con fallback monoespaciado."""
    font = QFont()
    font.setFamily(ensure_roboto_mono_registered())
    font.setPointSize(point_size)
    font.setBold(bold)
    if bold:
        font.setWeight(QFont.Weight.Bold)
    return font