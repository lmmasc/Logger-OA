"""
menu_bar.py

Módulo para definir y gestionar la barra de menús principal de la aplicación.
Permite separar la lógica del menú de la ventana principal para mayor modularidad.
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from app.translation import tr


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
        self.file_menu = QMenu(tr("file_menu"), self)
        self.open_folder_action = QAction(tr("open_folder"), self)
        self.file_menu.addAction(self.open_folder_action)
        self.exit_action = QAction(tr("exit"), self)
        self.file_menu.addAction(self.exit_action)
        self.addMenu(self.file_menu)

        # Menú Operativo
        # Contiene acciones relacionadas con operaciones no competitivas.
        self.operativo_menu = QMenu(tr("ops_menu"), self)
        self.ops_new_action = QAction(tr("new"), self)
        self.ops_open_action = QAction(tr("open"), self)
        self.ops_export_action = QAction(tr("export"), self)
        self.ops_close_action = QAction(tr("close"), self)
        self.operativo_menu.addAction(self.ops_new_action)
        self.operativo_menu.addAction(self.ops_open_action)
        self.operativo_menu.addAction(self.ops_export_action)
        self.operativo_menu.addAction(self.ops_close_action)
        self.addMenu(self.operativo_menu)

        # Menú Concurso
        # Contiene acciones específicas para gestión de concursos.
        self.concurso_menu = QMenu(tr("contest_menu"), self)
        self.contest_new_action = QAction(tr("new"), self)
        self.contest_open_action = QAction(tr("open"), self)
        self.contest_export_action = QAction(tr("export"), self)
        self.contest_close_action = QAction(tr("close"), self)
        self.concurso_menu.addAction(self.contest_new_action)
        self.concurso_menu.addAction(self.contest_open_action)
        self.concurso_menu.addAction(self.contest_export_action)
        self.concurso_menu.addAction(self.contest_close_action)
        self.addMenu(self.concurso_menu)

        # Menú Base de datos
        # Acciones de importación, exportación y visualización de la base de datos.
        self.database_menu = QMenu(tr("database_menu"), self)
        self.db_import_pdf_action = QAction(tr("import_from_pdf"), self)
        self.db_export_action = QAction(tr("export"), self)
        self.db_show_action = QAction(tr("show_database"), self)
        self.database_menu.addAction(self.db_import_pdf_action)
        self.database_menu.addAction(self.db_export_action)
        self.database_menu.addAction(self.db_show_action)
        self.addMenu(self.database_menu)

        # Menú Aspecto
        self.aspect_menu = QMenu(tr("aspect_menu"), self)
        self.light_theme_action = QAction(tr("light_theme"), self)
        self.dark_theme_action = QAction(tr("dark_theme"), self)
        self.light_theme_action.setCheckable(True)
        self.dark_theme_action.setCheckable(True)
        self.aspect_menu.addAction(self.light_theme_action)
        self.aspect_menu.addAction(self.dark_theme_action)
        self.addMenu(self.aspect_menu)

        # Menú Idioma
        self.language_menu = QMenu(tr("language_menu"), self)
        self.lang_es_action = QAction(tr("spanish"), self)
        self.lang_en_action = QAction(tr("english"), self)
        self.lang_es_action.setCheckable(True)
        self.lang_en_action.setCheckable(True)
        self.language_menu.addAction(self.lang_es_action)
        self.language_menu.addAction(self.lang_en_action)
        self.addMenu(self.language_menu)

        # Menú Ayuda
        self.help_menu = QMenu(tr("help_menu"), self)
        self.about_action = QAction(tr("about"), self)
        self.help_menu.addAction(self.about_action)
        self.addMenu(self.help_menu)
