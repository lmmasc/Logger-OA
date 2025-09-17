"""
theme_manager.py

Módulo para gestionar y aplicar temas (claro/oscuro) usando archivos QSS.
Utiliza settings_service para guardar y recuperar la preferencia del usuario.
"""

import os
from PySide6.QtWidgets import QApplication
from config.settings_service import settings_service, SettingsKey, ThemeValue
from utils.resources import get_resource_path


class ThemeManager:
    """
    Clase para gestionar y aplicar temas de la aplicación.
    Permite cambiar entre tema claro y oscuro, y guarda la preferencia del usuario.
    """

    def __init__(self):
        self.settings = settings_service
        self.theme_dir = os.path.dirname(__file__)
        theme_str = self.settings.get_value(
            SettingsKey.THEME.value, ThemeValue.LIGHT.value
        )
        self.current_theme = ThemeValue(theme_str)

    def apply_theme(self, theme: ThemeValue):
        """
        Carga y aplica el archivo QSS correspondiente al tema.
        Si el tema es AUTO, detecta el tema del sistema y lo aplica.
        Guarda la preferencia del usuario solo si realmente cambió.
        Args:
            theme (ThemeValue): ThemeValue.LIGHT, ThemeValue.DARK o ThemeValue.AUTO
        """
        if theme == ThemeValue.AUTO:
            from .system_theme import detect_system_theme

            detected_theme = detect_system_theme()
            theme_to_apply = detected_theme
        else:
            theme_to_apply = theme
        qss_rel_path = f"src/interface_adapters/ui/themes/{theme_to_apply.value}.qss"
        qss_path = get_resource_path(qss_rel_path)
        try:
            with open(qss_path, "r") as f:
                qss = f.read()
                app_instance = QApplication.instance()
                if isinstance(app_instance, QApplication):
                    app_instance.setStyleSheet(qss)
            if self.current_theme != theme:
                self.settings.set_value(SettingsKey.THEME.value, theme.value)
            self.current_theme = theme
        except Exception as e:
            raise RuntimeError(f"Error aplicando tema: {e}")

    def load_last_theme(self):
        """
        Carga y aplica el último tema usado por el usuario.
        Si el tema guardado es AUTO, detecta y aplica el tema del sistema.
        """
        theme_str = self.settings.get_value(
            SettingsKey.THEME.value, ThemeValue.LIGHT.value
        )
        theme = ThemeValue(theme_str)
        self.apply_theme(theme)
