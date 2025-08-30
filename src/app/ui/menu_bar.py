"""
menu_bar.py

Módulo para definir y gestionar la barra de menús principal de la aplicación.
Permite separar la lógica del menú de la ventana principal para mayor modularidad.
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from app.ui.translations import tr


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
        file_menu = QMenu(tr("file_menu"), self)
        self.exit_action = QAction(tr("exit"), self)
        file_menu.addAction(self.exit_action)
        self.addMenu(file_menu)

        # Menú Aspecto
        aspect_menu = QMenu(tr("aspect_menu"), self)
        self.light_theme_action = QAction(tr("light_theme"), self)
        self.dark_theme_action = QAction(tr("dark_theme"), self)
        self.light_theme_action.setCheckable(True)
        self.dark_theme_action.setCheckable(True)
        aspect_menu.addAction(self.light_theme_action)
        aspect_menu.addAction(self.dark_theme_action)
        self.addMenu(aspect_menu)

        # Menú Ayuda
        help_menu = QMenu(tr("help_menu"), self)
        self.about_action = QAction(tr("about"), self)
        help_menu.addAction(self.about_action)
        self.addMenu(help_menu)

        # Menú Idioma
        language_menu = QMenu(tr("language_menu"), self)
        self.lang_es_action = QAction(tr("spanish"), self)
        self.lang_en_action = QAction(tr("english"), self)
        self.lang_es_action.setCheckable(True)
        self.lang_en_action.setCheckable(True)
        language_menu.addAction(self.lang_es_action)
        language_menu.addAction(self.lang_en_action)
        self.addMenu(language_menu)
