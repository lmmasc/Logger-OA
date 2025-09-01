"""
menu_bar.py

Módulo para definir y gestionar la barra de menús principal de la aplicación.
Permite separar la lógica del menú de la ventana principal para mayor modularidad.
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal
from app.core.translation.translation_service import translation_service


class MainMenuBar(QMenuBar):
    """
    Barra de menús principal de la aplicación.
    Define los menús y acciones principales.
    Expone señales personalizadas para desacoplar la lógica de UI.
    """

    # Señales personalizadas para cada acción relevante
    ops_new_requested = Signal()
    ops_open_requested = Signal()
    ops_export_requested = Signal()
    ops_close_requested = Signal()
    contest_new_requested = Signal()
    contest_open_requested = Signal()
    contest_export_requested = Signal()
    contest_close_requested = Signal()
    db_import_pdf_requested = Signal()
    db_export_requested = Signal()
    db_show_requested = Signal()
    open_folder_requested = Signal()
    about_requested = Signal()
    exit_requested = Signal()
    light_theme_requested = Signal()
    dark_theme_requested = Signal()
    lang_es_requested = Signal()
    lang_en_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_menus()
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self._connect_signals()

    def _create_menus(self):
        # Menú Archivo
        self.file_menu = QMenu(translation_service.tr("file_menu"), self)
        self.open_folder_action = QAction(translation_service.tr("open_folder"), self)
        self.file_menu.addAction(self.open_folder_action)
        self.exit_action = QAction(translation_service.tr("exit"), self)
        self.file_menu.addAction(self.exit_action)
        self.addMenu(self.file_menu)

        # Menú Operativo
        self.operativo_menu = QMenu(translation_service.tr("ops_menu"), self)
        self.ops_new_action = QAction(translation_service.tr("new"), self)
        self.ops_open_action = QAction(translation_service.tr("open"), self)
        self.ops_export_action = QAction(translation_service.tr("export"), self)
        self.ops_close_action = QAction(translation_service.tr("close"), self)
        self.operativo_menu.addAction(self.ops_new_action)
        self.operativo_menu.addAction(self.ops_open_action)
        self.operativo_menu.addAction(self.ops_export_action)
        self.operativo_menu.addAction(self.ops_close_action)
        self.addMenu(self.operativo_menu)

        # Menú Concurso
        self.concurso_menu = QMenu(translation_service.tr("contest_menu"), self)
        self.contest_new_action = QAction(translation_service.tr("new"), self)
        self.contest_open_action = QAction(translation_service.tr("open"), self)
        self.contest_export_action = QAction(translation_service.tr("export"), self)
        self.contest_close_action = QAction(translation_service.tr("close"), self)
        self.concurso_menu.addAction(self.contest_new_action)
        self.concurso_menu.addAction(self.contest_open_action)
        self.concurso_menu.addAction(self.contest_export_action)
        self.concurso_menu.addAction(self.contest_close_action)
        self.addMenu(self.concurso_menu)

        # Menú Base de datos
        self.database_menu = QMenu(translation_service.tr("database_menu"), self)
        self.db_import_pdf_action = QAction(
            translation_service.tr("import_from_pdf"), self
        )
        self.db_export_action = QAction(translation_service.tr("export"), self)
        self.db_show_action = QAction(translation_service.tr("show_database"), self)
        self.database_menu.addAction(self.db_import_pdf_action)
        self.database_menu.addAction(self.db_export_action)
        self.database_menu.addAction(self.db_show_action)
        self.addMenu(self.database_menu)

        # Menú Aspecto
        self.aspect_menu = QMenu(translation_service.tr("aspect_menu"), self)
        self.light_theme_action = QAction(translation_service.tr("light_theme"), self)
        self.dark_theme_action = QAction(translation_service.tr("dark_theme"), self)
        self.light_theme_action.setCheckable(True)
        self.dark_theme_action.setCheckable(True)
        self.aspect_menu.addAction(self.light_theme_action)
        self.aspect_menu.addAction(self.dark_theme_action)
        self.addMenu(self.aspect_menu)

        # Menú Idioma
        self.language_menu = QMenu(translation_service.tr("language_menu"), self)
        self.lang_es_action = QAction(translation_service.tr("spanish"), self)
        self.lang_en_action = QAction(translation_service.tr("english"), self)
        self.lang_es_action.setCheckable(True)
        self.lang_en_action.setCheckable(True)
        self.language_menu.addAction(self.lang_es_action)
        self.language_menu.addAction(self.lang_en_action)
        self.addMenu(self.language_menu)

        # Menú Ayuda
        self.help_menu = QMenu(translation_service.tr("help_menu"), self)
        self.about_action = QAction(translation_service.tr("about"), self)
        self.help_menu.addAction(self.about_action)
        self.addMenu(self.help_menu)

    def _connect_signals(self):
        """
        Conecta las acciones del menú a las señales personalizadas.
        """
        self.ops_new_action.triggered.connect(self.ops_new_requested.emit)
        self.ops_open_action.triggered.connect(self.ops_open_requested.emit)
        self.ops_export_action.triggered.connect(self.ops_export_requested.emit)
        self.ops_close_action.triggered.connect(self.ops_close_requested.emit)
        self.contest_new_action.triggered.connect(self.contest_new_requested.emit)
        self.contest_open_action.triggered.connect(self.contest_open_requested.emit)
        self.contest_export_action.triggered.connect(self.contest_export_requested.emit)
        self.contest_close_action.triggered.connect(self.contest_close_requested.emit)
        self.db_import_pdf_action.triggered.connect(self.db_import_pdf_requested.emit)
        self.db_export_action.triggered.connect(self.db_export_requested.emit)
        self.db_show_action.triggered.connect(self.db_show_requested.emit)
        self.open_folder_action.triggered.connect(self.open_folder_requested.emit)
        self.about_action.triggered.connect(self.about_requested.emit)
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.light_theme_action.triggered.connect(self.light_theme_requested.emit)
        self.dark_theme_action.triggered.connect(self.dark_theme_requested.emit)
        self.lang_es_action.triggered.connect(self.lang_es_requested.emit)
        self.lang_en_action.triggered.connect(self.lang_en_requested.emit)

    def retranslate_ui(self):
        """
        Actualiza los textos de todos los menús y acciones según el idioma actual.
        """
        self.file_menu.setTitle(translation_service.tr("file_menu"))
        self.open_folder_action.setText(translation_service.tr("open_folder"))
        self.exit_action.setText(translation_service.tr("exit"))

        self.operativo_menu.setTitle(translation_service.tr("ops_menu"))
        self.ops_new_action.setText(translation_service.tr("new"))
        self.ops_open_action.setText(translation_service.tr("open"))
        self.ops_export_action.setText(translation_service.tr("export"))
        self.ops_close_action.setText(translation_service.tr("close"))

        self.concurso_menu.setTitle(translation_service.tr("contest_menu"))
        self.contest_new_action.setText(translation_service.tr("new"))
        self.contest_open_action.setText(translation_service.tr("open"))
        self.contest_export_action.setText(translation_service.tr("export"))
        self.contest_close_action.setText(translation_service.tr("close"))

        self.database_menu.setTitle(translation_service.tr("database_menu"))
        self.db_import_pdf_action.setText(translation_service.tr("import_from_pdf"))
        self.db_export_action.setText(translation_service.tr("export"))
        self.db_show_action.setText(translation_service.tr("show_database"))

        self.aspect_menu.setTitle(translation_service.tr("aspect_menu"))
        self.light_theme_action.setText(translation_service.tr("light_theme"))
        self.dark_theme_action.setText(translation_service.tr("dark_theme"))

        self.language_menu.setTitle(translation_service.tr("language_menu"))
        self.lang_es_action.setText(translation_service.tr("spanish"))
        self.lang_en_action.setText(translation_service.tr("english"))

        self.help_menu.setTitle(translation_service.tr("help_menu"))
        self.about_action.setText(translation_service.tr("about"))
