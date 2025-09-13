# --- Imports estándar ---
import os

# --- Imports externos ---
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

# --- Imports de configuración y utilidades ---
from config.settings_service import settings_service
from config.paths import get_database_path, BASE_PATH

# --- Imports de traducción y temas ---
from translation.translation_service import translation_service
from .themes.theme_manager import ThemeManager

# --- Imports de UI y vistas ---
from .menu_bar import MainMenuBar
from .views.welcome_view import WelcomeView
from .views.log_ops_view import LogOpsView
from .views.log_contest_view import LogContestView
from .view_manager import ViewManager

from interface_adapters.controllers.database_controller import DatabaseController

# --- Imports de acciones, diálogos y gestión de ventana ---
from .main_window_actions import (
    action_log_new,
    action_log_open,
    action_log_export,
    action_log_close,
    action_db_import_pdf,
    action_db_export,
    action_db_delete,
)
from .main_window_dialogs import show_about_dialog, show_manual_dialog
from .main_window_config import (
    set_language,
    set_light_theme,
    set_dark_theme,
    _set_initial_theme_and_language,
    _update_theme_menu_checks,
    _update_language_menu_checks,
    refresh_ui,
    _retranslate_ui,
)
from .main_window_view_management import show_view as mw_show_view
from .main_window_db_window import show_db_window, on_db_table_window_closed

"""
Módulo de la ventana principal de la aplicación.

Contiene la clase MainWindow, que define la ventana principal usando PySide6.
"""


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.

    Hereda de QMainWindow y configura el título, tamaño inicial y la barra de menús.
    Permite cambiar el tema y el idioma, y muestra un diálogo de información.
    """

    def __init__(self):
        """
        Inicializa la ventana principal, configura el título, tamaño, barra de menús,
        gestor de temas y conecta las acciones del menú.
        """
        super().__init__()
        self.current_log = None  # Estado del log abierto (None si no hay log)
        self.current_log_type = None  # "ops" o "contest"

        # Leer idioma guardado o usar por defecto
        lang = settings_service.get_value("language", "es")
        translation_service.set_language(lang)
        self.setWindowTitle(
            translation_service.tr("main_window_title")
        )  # Título de la ventana
        self.resize(1200, 700)  # Solo tamaño inicial
        self.center()

        # Instancia única de la ventana de tabla de base de datos
        self.db_table_window = None

        # Crear y asignar la barra de menús
        self.menu_bar = MainMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Gestor de temas
        self.theme_manager = ThemeManager()
        self.theme_manager.load_last_theme()

        # --- Gestor de vistas ---
        self.view_manager = ViewManager(self)
        # Instanciar vistas solo una vez
        self.log_ops_view = LogOpsView(self)
        self.log_contest_view = LogContestView(self)
        self.view_manager.register_view("welcome", WelcomeView(self))
        self.view_manager.register_view("log_ops", self.log_ops_view)
        self.view_manager.register_view("log_contest", self.log_contest_view)
        self.setCentralWidget(self.view_manager.get_widget())
        self.view_manager.show_view("welcome")

        # Conectar acciones del menú de forma explícita
        self._connect_menu_actions()

        # --- CORRECCIONES Y MEJORAS ---
        # 1. show_view debe ser método de instancia (faltaba tras refactor)
        # 2. Al iniciar, actualizar checks de tema e idioma según configuración guardada
        # Llama este método al final del __init__
        _set_initial_theme_and_language(self)
        self.update_menu_state()  # Estado inicial del menú

        # Conectar actualización de cabecera al cambiar idioma
        translation_service.signal.language_changed.connect(self._on_language_changed)

    # =====================
    # Métodos públicos principales
    # =====================

    def show_view(self, view_name: str) -> None:
        mw_show_view(self, view_name)
        # Actualizar la tabla de contactos en la vista activa si hay un log abierto
        if self.current_log is not None:
            contacts = getattr(self.current_log, "contacts", [])
            if view_name == "log_ops" and hasattr(self.log_ops_view, "table_widget"):
                self.log_ops_view.table_widget.set_contacts(contacts)
            elif view_name == "log_contest" and hasattr(
                self.log_contest_view, "table_widget"
            ):
                self.log_contest_view.table_widget.set_contacts(contacts)
        # Actualizar cabecera de la vista activa
        if view_name == "log_contest" and self.current_log:
            self.log_contest_view.set_log_data(self.current_log)
        elif view_name == "log_ops" and self.current_log:
            self.log_ops_view.set_log_data(self.current_log)

    def set_language(self, lang: str) -> None:
        set_language(self, lang)

    def set_light_theme(self) -> None:
        set_light_theme(self)

    def set_dark_theme(self) -> None:
        set_dark_theme(self)

    def _set_initial_theme_and_language(self) -> None:
        _set_initial_theme_and_language(self)

    def _update_theme_menu_checks(self) -> None:
        _update_theme_menu_checks(self)

    def _update_language_menu_checks(self) -> None:
        _update_language_menu_checks(self)

    def refresh_ui(self) -> None:
        refresh_ui(self)

    def _retranslate_ui(self) -> None:
        _retranslate_ui(self)

    def update_menu_state(self):
        """
        Habilita/deshabilita las acciones del menú según el estado del log abierto.
        """
        log_open = self.current_log is not None
        self.menu_bar.log_new_action.setEnabled(not log_open)
        self.menu_bar.log_open_action.setEnabled(not log_open)
        self.menu_bar.log_export_action.setEnabled(log_open)
        self.menu_bar.log_close_action.setEnabled(log_open)

    # =====================
    # Métodos de conexión de menús y handlers de acciones
    # =====================

    def _connect_menu_actions(self) -> None:
        """
        Conecta las señales personalizadas de la barra de menús a los handlers de MainWindow.
        """
        self.menu_bar.exit_requested.connect(self.close)
        self.menu_bar.manual_requested.connect(lambda: show_manual_dialog(self))
        self.menu_bar.about_requested.connect(lambda: show_about_dialog(self))
        self.menu_bar.open_folder_requested.connect(self._open_data_folder)
        self.menu_bar.light_theme_requested.connect(self.set_light_theme)
        self.menu_bar.dark_theme_requested.connect(self.set_dark_theme)
        self.menu_bar.lang_es_requested.connect(lambda: self.set_language("es"))
        self.menu_bar.lang_en_requested.connect(lambda: self.set_language("en"))
        self.menu_bar.log_new_requested.connect(lambda: action_log_new(self))
        self.menu_bar.log_open_requested.connect(lambda: action_log_open(self))
        self.menu_bar.log_export_requested.connect(lambda: action_log_export(self))
        self.menu_bar.log_close_requested.connect(lambda: action_log_close(self))
        self.menu_bar.db_import_pdf_requested.connect(
            lambda: action_db_import_pdf(self)
        )
        self.menu_bar.db_export_requested.connect(lambda: action_db_export(self))
        self.menu_bar.db_delete_requested.connect(lambda: action_db_delete(self))
        self.menu_bar.db_show_requested.connect(self._show_db_window)
        # --- NUEVAS ACCIONES DE BASE DE DATOS ---
        self.menu_bar.db_backup_action.triggered.connect(self._on_db_backup)
        self.menu_bar.db_restore_action.triggered.connect(self._on_db_restore)
        self.menu_bar.db_import_db_action.triggered.connect(self._on_db_import_db)

    def _on_db_backup(self):
        try:
            backup_path = DatabaseController.backup_database()
            QMessageBox.information(self, "Backup", f"Backup creado en: {backup_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el backup: {e}")

    def _on_db_restore(self):
        from PySide6.QtWidgets import QFileDialog
        import os

        backup_dir = os.path.join(BASE_PATH, "backups")
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Seleccionar backup para restaurar")
        file_dialog.setDirectory(backup_dir)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Backups (*.db)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                backup_file = os.path.basename(selected_files[0])
                try:
                    DatabaseController.restore_database(backup_file)
                    QMessageBox.information(
                        self, "Restaurar", f"Base restaurada desde: {backup_file}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo restaurar: {e}")

    def _on_db_import_db(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Bases de datos (*.db)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                external_db_path = selected_files[0]
                try:
                    imported = DatabaseController.import_database(external_db_path)
                    QMessageBox.information(
                        self, "Importar", f"Operadores importados: {imported}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo importar: {e}")

    def _open_data_folder(self) -> None:
        """
        Abre la carpeta donde se guarda la base de datos.
        """
        db_path = get_database_path()
        folder = os.path.dirname(db_path)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    def center(self):
        """
        Centra la ventana en la pantalla principal.
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    # ...existing code...

    # =====================
    # Métodos de gestión de ventanas secundarias
    # =====================

    def _show_db_window(self):
        show_db_window(self)

    def _on_db_table_window_closed(self, *args):
        on_db_table_window_closed(self, *args)

    def closeEvent(self, event):
        # Cerrar la ventana de tabla de base de datos si está abierta
        if self.db_table_window is not None:
            self.db_table_window.close()
        super().closeEvent(event)

    def _on_language_changed(self):
        # Llama retranslate_ui en la vista activa
        if self.current_log_type == "contest":
            self.log_contest_view.retranslate_ui()
        elif self.current_log_type == "ops":
            self.log_ops_view.retranslate_ui()
