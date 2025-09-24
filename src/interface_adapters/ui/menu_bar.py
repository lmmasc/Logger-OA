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
    lang_auto_requested = Signal()
    manual_requested = Signal()
    log_new_operativo_requested = Signal()
    log_new_concurso_requested = Signal()
    log_open_operativo_requested = Signal()
    log_open_concurso_requested = Signal()
    log_export_txt_requested = Signal()
    log_export_csv_requested = Signal()
    log_export_adi_requested = Signal()
    log_export_pdf_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_menus()
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self._connect_signals()

    def _create_menus(self):
        # Menú Archivo (ahora incluye acciones de Log)
        self.file_menu = QMenu(translation_service.tr("menu_file_menu"), self)
        # Submenú Nuevo
        self.new_menu = QMenu(translation_service.tr("menu_new"), self.file_menu)
        self.log_new_operativo_action = QAction(
            translation_service.tr("menu_new_operativo"), self
        )
        self.log_new_concurso_action = QAction(
            translation_service.tr("menu_new_concurso"), self
        )
        self.new_menu.addAction(self.log_new_operativo_action)
        self.new_menu.addAction(self.log_new_concurso_action)
        self.file_menu.addMenu(self.new_menu)

        # Submenú Abrir
        self.open_menu = QMenu(translation_service.tr("menu_open"), self.file_menu)
        self.log_open_operativo_action = QAction(
            translation_service.tr("menu_open_operativo"), self
        )
        self.log_open_concurso_action = QAction(
            translation_service.tr("menu_open_concurso"), self
        )
        self.open_menu.addAction(self.log_open_operativo_action)
        self.open_menu.addAction(self.log_open_concurso_action)
        self.file_menu.addMenu(self.open_menu)

        # Submenú Exportar
        self.export_menu = QMenu(translation_service.tr("menu_export"), self.file_menu)
        self.export_txt_action = QAction(
            translation_service.tr("menu_export_txt"), self
        )
        self.export_csv_action = QAction(
            translation_service.tr("menu_export_csv"), self
        )
        self.export_adi_action = QAction(
            translation_service.tr("menu_export_adi"), self
        )
        self.export_pdf_action = QAction(
            translation_service.tr("menu_export_pdf"), self
        )
        self.export_whatsapp_action = QAction("Whatsapp", self)
        self.export_menu.addAction(self.export_txt_action)
        self.export_menu.addAction(self.export_csv_action)
        self.export_menu.addAction(self.export_adi_action)
        self.export_menu.addAction(self.export_pdf_action)
        self.export_menu.addAction(self.export_whatsapp_action)
        self.file_menu.addMenu(self.export_menu)

        self.log_close_action = QAction(translation_service.tr("menu_close"), self)
        self.file_menu.addAction(self.log_close_action)
        self.file_menu.addSeparator()
        self.open_folder_action = QAction(
            translation_service.tr("menu_open_folder"), self
        )
        self.file_menu.addAction(self.open_folder_action)
        self.file_menu.addSeparator()
        self.exit_action = QAction(translation_service.tr("menu_exit"), self)
        self.file_menu.addAction(self.exit_action)
        self.addMenu(self.file_menu)

        # Menú Base de datos reorganizado
        self.database_menu = QMenu(translation_service.tr("menu_database_menu"), self)
        self.db_show_action = QAction(
            translation_service.tr("menu_show_database"), self
        )
        self.database_menu.addAction(self.db_show_action)

        # Submenú Importar
        self.import_menu = QMenu(
            translation_service.tr("menu_database_section_import"), self.database_menu
        )
        self.db_import_pdf_action = QAction(
            translation_service.tr("menu_import_from_pdf"), self
        )
        self.db_import_db_action = QAction(
            translation_service.tr("menu_import_from_db"), self
        )
        self.import_menu.addAction(self.db_import_pdf_action)
        self.import_menu.addAction(self.db_import_db_action)
        self.database_menu.addMenu(self.import_menu)

        # Submenú Backup
        self.backup_menu = QMenu(
            translation_service.tr("menu_database_section_backup"), self.database_menu
        )
        self.db_backup_action = QAction(
            translation_service.tr("menu_create_backup"), self
        )
        self.db_restore_action = QAction(
            translation_service.tr("menu_restore_backup"), self
        )
        self.backup_menu.addAction(self.db_backup_action)
        self.backup_menu.addAction(self.db_restore_action)
        self.database_menu.addMenu(self.backup_menu)

        # Submenú Exportar
        self.export_db_menu = QMenu(
            translation_service.tr("menu_database_section_export"), self.database_menu
        )
        self.db_export_action = QAction(
            translation_service.tr("menu_export_db_csv"), self
        )
        self.export_db_menu.addAction(self.db_export_action)
        self.database_menu.addMenu(self.export_db_menu)

        # Submenú Borrar
        self.delete_menu = QMenu(
            translation_service.tr("menu_database_section_delete"), self.database_menu
        )
        self.db_delete_action = QAction(
            translation_service.tr("menu_delete_database"), self
        )
        self.delete_menu.addAction(self.db_delete_action)
        self.database_menu.addMenu(self.delete_menu)

        self.addMenu(self.database_menu)

        # Menú Preferencias con submenús Indicativo, Aspecto e Idioma
        self.preferences_menu = QMenu(
            translation_service.tr("menu_preferences_menu"), self
        )
        # Indicative submenu in Preferences
        self.indicative_submenu = QMenu(
            translation_service.tr("menu_indicative_menu"), self.preferences_menu
        )
        self.set_callsign_action = QAction(
            translation_service.tr("menu_set_callsign"), self
        )
        self.set_callsign_action.setCheckable(False)
        self.indicative_submenu.addAction(self.set_callsign_action)
        self.indicative_submenu.addSeparator()
        self.callsign_saved_mode_action = QAction(
            translation_service.tr("menu_callsign_saved_mode"), self
        )
        self.callsign_saved_mode_action.setCheckable(True)
        self.callsign_always_ask_mode_action = QAction(
            translation_service.tr("menu_callsign_always_ask_mode"), self
        )
        self.callsign_always_ask_mode_action.setCheckable(True)
        self.indicative_submenu.addAction(self.callsign_saved_mode_action)
        self.indicative_submenu.addAction(self.callsign_always_ask_mode_action)
        self.indicative_submenu.addSeparator()
        self.callsign_display_action = QAction(
            translation_service.tr("menu_callsign_display"), self
        )
        self.callsign_display_action.setEnabled(False)
        self.indicative_submenu.addAction(self.callsign_display_action)
        self.preferences_menu.addMenu(self.indicative_submenu)

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
        self.lang_auto_action = QAction(
            translation_service.tr("menu_auto_language"), self
        )
        self.lang_es_action.setCheckable(True)
        self.lang_en_action.setCheckable(True)
        self.lang_auto_action.setCheckable(True)
        self.language_submenu.addAction(self.lang_es_action)
        self.language_submenu.addAction(self.lang_en_action)
        self.language_submenu.addAction(self.lang_auto_action)
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
        self.log_new_operativo_action.triggered.connect(
            self.log_new_operativo_requested.emit
        )
        self.log_new_concurso_action.triggered.connect(
            self.log_new_concurso_requested.emit
        )
        self.log_open_operativo_action.triggered.connect(
            self.log_open_operativo_requested.emit
        )
        self.log_open_concurso_action.triggered.connect(
            self.log_open_concurso_requested.emit
        )
        self.log_close_action.triggered.connect(self.log_close_requested.emit)
        self.db_import_pdf_action.triggered.connect(self.db_import_pdf_requested.emit)
        self.db_export_action.triggered.connect(self.db_export_requested.emit)
        self.db_show_action.triggered.connect(self.db_show_requested.emit)
        self.db_delete_action.triggered.connect(self.db_delete_requested.emit)
        self.open_folder_action.triggered.connect(self.open_folder_requested.emit)
        self.about_action.triggered.connect(self.about_requested.emit)
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.light_theme_action.triggered.connect(self.light_theme_requested.emit)
        self.dark_theme_action.triggered.connect(self.dark_theme_requested.emit)
        self.auto_theme_action.triggered.connect(self.auto_theme_requested.emit)
        self.lang_es_action.triggered.connect(self.lang_es_requested.emit)
        self.lang_en_action.triggered.connect(self.lang_en_requested.emit)
        self.lang_auto_action.triggered.connect(self.lang_auto_requested.emit)
        self.manual_action.triggered.connect(self.manual_requested.emit)
        self.export_txt_action.triggered.connect(self.log_export_txt_requested.emit)
        self.export_csv_action.triggered.connect(self.log_export_csv_requested.emit)
        self.export_adi_action.triggered.connect(self.log_export_adi_requested.emit)
        self.export_pdf_action.triggered.connect(self.log_export_pdf_requested.emit)

    def retranslate_ui(self):
        self.file_menu.setTitle(translation_service.tr("menu_file_menu"))
        self.open_folder_action.setText(translation_service.tr("menu_open_folder"))
        self.exit_action.setText(translation_service.tr("menu_exit"))
        self.new_menu.setTitle(translation_service.tr("menu_new"))
        self.log_new_operativo_action.setText(
            translation_service.tr("menu_new_operativo")
        )
        self.log_new_concurso_action.setText(
            translation_service.tr("menu_new_concurso")
        )
        self.open_menu.setTitle(translation_service.tr("menu_open"))
        self.log_open_operativo_action.setText(
            translation_service.tr("menu_open_operativo")
        )
        self.log_open_concurso_action.setText(
            translation_service.tr("menu_open_concurso")
        )
        self.log_close_action.setText(translation_service.tr("menu_close"))

        self.export_menu.setTitle(translation_service.tr("menu_export"))

        self.export_txt_action.setText(translation_service.tr("menu_export_txt"))
        self.export_csv_action.setText(translation_service.tr("menu_export_csv"))
        self.export_adi_action.setText(translation_service.tr("menu_export_adi"))
        self.export_pdf_action.setText(translation_service.tr("menu_export_pdf"))

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
        self.lang_auto_action.setText(translation_service.tr("menu_auto_language"))
        self.indicative_submenu.setTitle(translation_service.tr("menu_indicative_menu"))
        self.set_callsign_action.setText(translation_service.tr("menu_set_callsign"))
        self.callsign_saved_mode_action.setText(
            translation_service.tr("menu_callsign_saved_mode")
        )
        self.callsign_always_ask_mode_action.setText(
            translation_service.tr("menu_callsign_always_ask_mode")
        )
        self.callsign_display_action.setText(
            translation_service.tr("menu_callsign_display")
        )

        self.help_menu.setTitle(translation_service.tr("menu_help_menu"))
        self.about_action.setText(translation_service.tr("menu_about"))
        self.manual_action.setText(translation_service.tr("menu_manual"))
