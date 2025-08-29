"""
theme_manager.py

Módulo para gestionar y aplicar temas (claro/oscuro) usando archivos QSS.
Utiliza SettingsManager para guardar y recuperar la preferencia del usuario.
"""

import os
from PySide6.QtWidgets import QApplication
from app.config.settings_manager import SettingsManager


class ThemeManager:
    """
    Clase para gestionar y aplicar temas de la aplicación.
    Permite cambiar entre tema claro y oscuro, y guarda la preferencia del usuario.
    """

    def __init__(self):
        self.settings = SettingsManager()
        self.theme_dir = os.path.join(os.path.dirname(__file__))
        self.current_theme = self.settings.get_value("theme", "light")

    def apply_theme(self, theme_name: str):
        """
        Carga y aplica el archivo QSS correspondiente al tema.
        Guarda la preferencia del usuario.
        Args:
            theme_name (str): "light" o "dark"
        """
        qss_path = os.path.join(self.theme_dir, f"{theme_name}.qss")
        try:
            with open(qss_path, "r") as f:
                qss = f.read()
                QApplication.instance().setStyleSheet(qss)
                self.current_theme = theme_name
                self.settings.set_value("theme", theme_name)
        except Exception as e:
            print(f"Error aplicando tema: {e}")

    def load_last_theme(self):
        """
        Carga y aplica el último tema usado por el usuario.
        """
        self.apply_theme(self.current_theme)
