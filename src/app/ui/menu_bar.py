"""
menu_bar.py

Módulo para definir y gestionar la barra de menús principal de la aplicación.
Permite separar la lógica del menú de la ventana principal para mayor modularidad.
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction


class MainMenuBar(QMenuBar):
    """
    Barra de menús principal de la aplicación.
    Define los menús y acciones principales.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_menus()

    def _create_menus(self):
        # Menú Archivo
        file_menu = QMenu("Archivo", self)
        self.exit_action = QAction("Salir", self)
        file_menu.addAction(self.exit_action)
        self.addMenu(file_menu)

        # Menú Aspecto
        aspect_menu = QMenu("Aspecto", self)
        self.light_theme_action = QAction("Tema claro", self)
        self.dark_theme_action = QAction("Tema oscuro", self)
        self.light_theme_action.setCheckable(True)
        self.dark_theme_action.setCheckable(True)
        aspect_menu.addAction(self.light_theme_action)
        aspect_menu.addAction(self.dark_theme_action)
        self.addMenu(aspect_menu)

        # Menú Ayuda
        help_menu = QMenu("Ayuda", self)
        self.about_action = QAction("Acerca de", self)
        help_menu.addAction(self.about_action)
        self.addMenu(help_menu)
