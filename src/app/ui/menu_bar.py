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
        exit_action = QAction("Salir", self)
        file_menu.addAction(exit_action)
        self.addMenu(file_menu)

        # Menú Ayuda
        help_menu = QMenu("Ayuda", self)
        about_action = QAction("Acerca de", self)
        help_menu.addAction(about_action)
        self.addMenu(help_menu)

        # Puedes conectar las acciones aquí o desde la ventana principal
        # exit_action.triggered.connect(...)
        # about_action.triggered.connect(...)
