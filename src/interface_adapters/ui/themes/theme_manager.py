"""
theme_manager.py

Módulo para gestionar y aplicar temas (claro/oscuro) usando archivos QSS.
Utiliza settings_service para guardar y recuperar la preferencia del usuario.
"""

import os
from PySide6.QtWidgets import QApplication
from config.settings_service import settings_service
from utils.resources import get_resource_path


class ThemeManager:
    """
    Clase para gestionar y aplicar temas de la aplicación.
    Permite cambiar entre tema claro y oscuro, y guarda la preferencia del usuario.
    """

    def __init__(self):
        self.settings = settings_service
        self.theme_dir = os.path.dirname(__file__)
        self.current_theme = self.settings.get_value("theme", "light")

    def apply_theme(self, theme_name: str):
        """
        Carga y aplica el archivo QSS correspondiente al tema.
        Guarda la preferencia del usuario solo si realmente cambió.
        Args:
            theme_name (str): "light" o "dark"
        """
        qss_rel_path = f"src/interface_adapters/ui/themes/{theme_name}.qss"
        qss_path = get_resource_path(qss_rel_path)
        try:
            with open(qss_path, "r") as f:
                qss = f.read()
                QApplication.instance().setStyleSheet(qss)
            # Solo guardar si el valor cambió
            if self.current_theme != theme_name:
                self.settings.set_value("theme", theme_name)
            self.current_theme = theme_name
        except Exception as e:
            raise RuntimeError(f"Error aplicando tema: {e}")

    def load_last_theme(self):
        """
        Carga y aplica el último tema usado por el usuario.
        """
        self.apply_theme(self.current_theme)
