"""
menu_bar.py

Módulo para definir y gestionar la barra de menús principal de la aplicación.
Permite separar la lógica del menú de la ventana principal para mayor modularidad.
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal
from translation.translation_service import translation_service


class MainMenuBar(QMenuBar):
    """
    Barra de menús principal de la aplicación.
    Define los menús y acciones principales.
    Expone señales personalizadas para desacoplar la lógica de UI.
    """

    # Señales personalizadas para acciones de log unificadas
    log_new_requested = Signal()
    log_open_requested = Signal()
    log_export_requested = Signal()
    log_close_requested = Signal()
    db_import_pdf_requested = Signal()
    db_export_requested = Signal()
    db_show_requested = Signal()
    db_delete_requested = Signal()
    open_folder_requested = Signal()
    about_requested = Signal()
    exit_requested = Signal()
    light_theme_requested = Signal()
    dark_theme_requested = Signal()
    auto_theme_requested = Signal()
    lang_es_requested = Signal()
    lang_en_requested = Signal()
    manual_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_menus()
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self._connect_signals()

    def _create_menus(self):
        # Menú Archivo
        self.file_menu = QMenu(translation_service.tr("menu_file_menu"), self)
        self.open_folder_action = QAction(
            translation_service.tr("menu_open_folder"), self
        )
        self.file_menu.addAction(self.open_folder_action)
        self.exit_action = QAction(translation_service.tr("menu_exit"), self)
        self.file_menu.addAction(self.exit_action)
        self.addMenu(self.file_menu)

        # Menú Log unificado
        self.log_menu = QMenu(translation_service.tr("menu_log_menu"), self)
        self.log_new_action = QAction(translation_service.tr("menu_new"), self)
        self.log_open_action = QAction(translation_service.tr("menu_open"), self)
        self.log_export_action = QAction(translation_service.tr("menu_export"), self)
        self.log_close_action = QAction(translation_service.tr("menu_close"), self)
        self.log_menu.addAction(self.log_new_action)
        self.log_menu.addAction(self.log_open_action)
        self.log_menu.addAction(self.log_export_action)
        self.log_menu.addAction(self.log_close_action)
        self.addMenu(self.log_menu)

        # Menú Base de datos
        self.database_menu = QMenu(translation_service.tr("menu_database_menu"), self)
        self.db_import_pdf_action = QAction(
            translation_service.tr("menu_import_from_pdf"), self
        )
        self.db_import_db_action = QAction(
            translation_service.tr("menu_import_from_db"), self
        )
        self.db_backup_action = QAction(
            translation_service.tr("menu_create_backup"), self
        )
        self.db_restore_action = QAction(
            translation_service.tr("menu_restore_backup"), self
        )
        self.db_export_action = QAction(
            translation_service.tr("menu_export_db_csv"), self
        )
        self.db_show_action = QAction(
            translation_service.tr("menu_show_database"), self
        )
        self.db_delete_action = QAction(
            translation_service.tr("menu_delete_database"), self
        )
        # Sección de visualización
        self.database_menu.addSection(translation_service.tr("menu_show_database"))
        self.database_menu.addAction(self.db_show_action)
        # Sección de importación
        self.database_menu.addSection(
            translation_service.tr("menu_database_section_import")
        )
        self.database_menu.addAction(self.db_import_pdf_action)
        self.database_menu.addAction(self.db_import_db_action)
        # Sección de respaldo
        self.database_menu.addSection(
            translation_service.tr("menu_database_section_backup")
        )
        self.database_menu.addAction(self.db_backup_action)
        self.database_menu.addAction(self.db_restore_action)
        # Sección de exportación
        self.database_menu.addSection(translation_service.tr("menu_export_db_csv"))
        self.database_menu.addAction(self.db_export_action)
        # Espacio en blanco antes del separador y la opción de borrar
        self.database_menu.addAction(QAction(" ", self))
        self.database_menu.addSeparator()
        self.database_menu.addAction(self.db_delete_action)
        self.addMenu(self.database_menu)

        # Menú Preferencias con submenús Aspecto e Idioma
        self.preferences_menu = QMenu(
            translation_service.tr("menu_preferences_menu"), self
        )
        # Submenú Aspecto
        self.aspect_submenu = QMenu(
            translation_service.tr("menu_aspect_menu"), self.preferences_menu
        )
        self.light_theme_action = QAction(
            translation_service.tr("menu_light_theme"), self
        )
        self.dark_theme_action = QAction(
            translation_service.tr("menu_dark_theme"), self
        )
        self.auto_theme_action = QAction(
            translation_service.tr("menu_auto_theme"), self
        )
        self.light_theme_action.setCheckable(True)
        self.dark_theme_action.setCheckable(True)
        self.auto_theme_action.setCheckable(True)
        self.aspect_submenu.addAction(self.light_theme_action)
        self.aspect_submenu.addAction(self.dark_theme_action)
        self.aspect_submenu.addAction(self.auto_theme_action)
        self.preferences_menu.addMenu(self.aspect_submenu)
        # Submenú Idioma
        self.language_submenu = QMenu(
            translation_service.tr("menu_language_menu"), self.preferences_menu
        )
        self.lang_es_action = QAction(translation_service.tr("menu_spanish"), self)
        self.lang_en_action = QAction(translation_service.tr("menu_english"), self)
        self.lang_es_action.setCheckable(True)
        self.lang_en_action.setCheckable(True)
        self.language_submenu.addAction(self.lang_es_action)
        self.language_submenu.addAction(self.lang_en_action)
        self.preferences_menu.addMenu(self.language_submenu)
        self.addMenu(self.preferences_menu)

        # Menú Ayuda
        self.help_menu = QMenu(translation_service.tr("menu_help_menu"), self)
        self.about_action = QAction(translation_service.tr("menu_about"), self)
        self.manual_action = QAction(translation_service.tr("menu_manual"), self)
        self.help_menu.addAction(self.manual_action)
        self.help_menu.addAction(self.about_action)
        self.addMenu(self.help_menu)

    def _connect_signals(self):
        """
        Conecta las acciones del menú a las señales personalizadas.
        """
        self.log_new_action.triggered.connect(self.log_new_requested.emit)
        self.log_open_action.triggered.connect(self.log_open_requested.emit)
        self.log_export_action.triggered.connect(self.log_export_requested.emit)
        self.log_close_action.triggered.connect(self.log_close_requested.emit)
        self.db_import_pdf_action.triggered.connect(self.db_import_pdf_requested.emit)
        self.db_export_action.triggered.connect(self.db_export_requested.emit)
        self.db_show_action.triggered.connect(self.db_show_requested.emit)
        self.db_delete_action.triggered.connect(self.db_delete_requested.emit)
        self.open_folder_action.triggered.connect(self.open_folder_requested.emit)
        self.about_action.triggered.connect(self.about_requested.emit)
        self.exit_action.triggered.connect(self.exit_requested.emit)
        # Preferencias (Aspecto e Idioma)
        self.light_theme_action.triggered.connect(self.light_theme_requested.emit)
        self.dark_theme_action.triggered.connect(self.dark_theme_requested.emit)
        self.auto_theme_action.triggered.connect(self.auto_theme_requested.emit)
        self.lang_es_action.triggered.connect(self.lang_es_requested.emit)
        self.lang_en_action.triggered.connect(self.lang_en_requested.emit)
        self.manual_action.triggered.connect(self.manual_requested.emit)

    def retranslate_ui(self):
        """
        Actualiza los textos de todos los menús y acciones según el idioma actual.
        """
        self.file_menu.setTitle(translation_service.tr("menu_file_menu"))
        self.open_folder_action.setText(translation_service.tr("menu_open_folder"))
        self.exit_action.setText(translation_service.tr("menu_exit"))
        self.log_menu.setTitle(translation_service.tr("menu_log_menu"))
        self.log_new_action.setText(translation_service.tr("menu_new"))
        self.log_open_action.setText(translation_service.tr("menu_open"))
        self.log_export_action.setText(translation_service.tr("menu_export"))
        self.log_close_action.setText(translation_service.tr("menu_close"))

        self.database_menu.setTitle(translation_service.tr("menu_database_menu"))
        self.db_import_pdf_action.setText(
            translation_service.tr("menu_import_from_pdf")
        )
        self.db_import_db_action.setText(translation_service.tr("menu_import_from_db"))
        self.db_backup_action.setText(translation_service.tr("menu_create_backup"))
        self.db_restore_action.setText(translation_service.tr("menu_restore_backup"))
        self.db_export_action.setText(translation_service.tr("menu_export_db_csv"))
        self.db_show_action.setText(translation_service.tr("menu_show_database"))
        self.db_delete_action.setText(translation_service.tr("menu_delete_database"))

        self.preferences_menu.setTitle(translation_service.tr("menu_preferences_menu"))
        self.aspect_submenu.setTitle(translation_service.tr("menu_aspect_menu"))
        self.light_theme_action.setText(translation_service.tr("menu_light_theme"))
        self.dark_theme_action.setText(translation_service.tr("menu_dark_theme"))
        self.auto_theme_action.setText(translation_service.tr("menu_auto_theme"))
        self.language_submenu.setTitle(translation_service.tr("menu_language_menu"))
        self.lang_es_action.setText(translation_service.tr("menu_spanish"))
        self.lang_en_action.setText(translation_service.tr("menu_english"))

        self.help_menu.setTitle(translation_service.tr("menu_help_menu"))
        self.about_action.setText(translation_service.tr("menu_about"))
        self.manual_action.setText(translation_service.tr("menu_manual"))
