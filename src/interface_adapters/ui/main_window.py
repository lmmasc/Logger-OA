"""
main_window.py
Ventana principal de Logger OA v2 (PySide6).
Gestiona la UI, menús, vistas, temas, idioma y delega acciones a main_window_actions.
"""

# Imports estándar
import os

# Imports externos
from PySide6.QtWidgets import QMainWindow, QApplication, QInputDialog

# Imports internos: configuración, traducción, UI, acciones
from config.settings_service import (
    settings_service,
    LanguageValue,
    SettingsKey,
    CallsignMode,
)
from utils.resources import get_resource_path
from translation.translation_service import translation_service
from .themes.theme_manager import ThemeManager
from .menu_bar import MainMenuBar
from .views.welcome_view import WelcomeView
from .views.log_ops_view import LogOpsView
from .views.log_contest_view import LogContestView
from .view_manager import ViewManager, ViewID, LogType
from .main_window_actions import (
    action_log_new_operativo,
    action_log_new_concurso,
    action_log_open_operativo,
    action_log_open_concurso,
    action_log_close,
    action_db_import_pdf,
    action_db_import_excel,
    action_db_export,
    action_db_delete,
    action_db_backup,
    action_db_restore,
    action_db_import_db,
    action_open_data_folder,
    action_show_db_window,
    action_on_db_table_window_closed,
    action_log_export_txt,
    action_log_export_csv,
    action_log_export_adi,
    action_log_export_pdf,
    action_log_export_simple_text,
)
from .main_window_dialogs import show_about_dialog, show_manual_dialog
from .main_window_config import (
    set_language,
    set_light_theme,
    set_dark_theme,
    set_initial_theme_and_language,
    update_theme_menu_checks,
    update_language_menu_checks,
    refresh_ui,
    retranslate_ui,
)


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación Logger OA v2.
    Gestiona la UI, menús, vistas, temas, idioma y delega acciones a main_window_actions.
    """

    def __init__(self):
        """
        Inicializa la ventana principal, configura título, tamaño, menús, temas, vistas y conecta señales.
        """
        super().__init__()
        # Icono multiplataforma
        from PySide6.QtGui import QIcon
        import sys

        if sys.platform.startswith("win"):
            self.setWindowIcon(QIcon(get_resource_path("assets/app_icon.ico")))
        else:
            self.setWindowIcon(QIcon(get_resource_path("assets/app_icon.png")))
        self.current_log = None  # Log abierto (None si no hay log)
        self.current_log_type = None  # LogType.OPERATION_LOG o LogType.CONTEST_LOG
        self.db_table_window = (
            None  # Instancia única de ventana de tabla de base de datos
        )
        self.manual_window = None  # Instancia única de ventana de manual de ayuda

        # Configuración de idioma y título
        lang = settings_service.get_value(
            SettingsKey.LANGUAGE.value, LanguageValue.ES.value
        )
        lang_enum = LanguageValue(lang)
        translation_service.set_language(lang_enum)
        self.setWindowTitle(translation_service.tr("main_window_title"))
        self.resize(1200, 700)
        self.center()

        # Barra de menús
        self.menu_bar = MainMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Gestor de temas
        self.theme_manager = ThemeManager()
        self.theme_manager.load_last_theme()

        # Gestor de vistas
        self.view_manager = ViewManager(self)
        self.log_ops_view = LogOpsView(self)
        self.log_contest_view = LogContestView(self)
        self.view_manager.register_view(ViewID.WELCOME_VIEW, WelcomeView(self))
        self.view_manager.register_view(ViewID.LOG_OPS_VIEW, self.log_ops_view)
        self.view_manager.register_view(ViewID.LOG_CONTEST_VIEW, self.log_contest_view)
        self.setCentralWidget(self.view_manager.get_widget())
        self.view_manager.show_view(ViewID.WELCOME_VIEW)

        # Conexión de acciones del menú
        self._connect_menu_actions()

        # Aplicar tema e idioma guardados
        set_initial_theme_and_language(self)
        self.update_menu_state()

        # Actualizar cabecera al cambiar idioma
        translation_service.signal.language_changed.connect(self._on_language_changed)

        # Inicializar estado del submenú Indicative
        self._set_initial_callsign_menu_state()

    # --- Gestión de vistas principales ---
    def show_view(self, view_id: ViewID) -> None:
        """
        Muestra la vista indicada y actualiza datos de contactos y cabecera si hay log abierto.
        """
        self.view_manager.show_view(view_id)
        if self.current_log is not None:
            contacts = getattr(self.current_log, "contacts", [])
            if view_id == ViewID.LOG_OPS_VIEW and hasattr(
                self.log_ops_view, "table_widget"
            ):
                self.log_ops_view.table_widget.set_contacts(contacts)
            elif view_id == ViewID.LOG_CONTEST_VIEW and hasattr(
                self.log_contest_view, "table_widget"
            ):
                self.log_contest_view.table_widget.set_contacts(contacts)
        if view_id == ViewID.LOG_CONTEST_VIEW and self.current_log:
            self.log_contest_view.set_log_data(self.current_log)
        elif view_id == ViewID.LOG_OPS_VIEW and self.current_log:
            self.log_ops_view.set_log_data(self.current_log)

    # --- Gestión de temas e idioma ---
    def set_language(self, lang: LanguageValue) -> None:
        """
        Cambia el idioma de la interfaz.
        """
        set_language(self, lang)

    def set_light_theme(self) -> None:
        """
        Cambia la interfaz al tema claro.
        """
        set_light_theme(self)

    def set_dark_theme(self) -> None:
        """
        Cambia la interfaz al tema oscuro.
        """
        set_dark_theme(self)

    def _set_initial_theme_and_language(self) -> None:
        """
        Aplica el tema e idioma guardados al iniciar la aplicación.
        """
        set_initial_theme_and_language(self)

    def update_theme_menu_checks(self) -> None:
        """
        Actualiza los checks del menú de tema según el tema activo.
        """
        update_theme_menu_checks(self)

    def update_language_menu_checks(self) -> None:
        """
        Actualiza los checks del menú de idioma según el idioma activo.
        """
        update_language_menu_checks(self)

    def refresh_ui(self) -> None:
        """
        Refresca la interfaz gráfica (traducción, colores, etc).
        """
        refresh_ui(self)

    def _retranslate_ui(self) -> None:
        """
        Retraduce la interfaz gráfica al cambiar el idioma.
        """
        retranslate_ui(self)

    # --- Gestión de menú y acciones ---
    def update_menu_state(self):
        """
        Habilita/deshabilita las acciones del menú según el estado del log abierto.
        """
        log_open = self.current_log is not None
        # Deshabilitar acciones internas
        self.menu_bar.log_new_operativo_action.setEnabled(not log_open)
        self.menu_bar.log_new_concurso_action.setEnabled(not log_open)
        self.menu_bar.log_open_operativo_action.setEnabled(not log_open)
        self.menu_bar.log_open_concurso_action.setEnabled(not log_open)
        # Deshabilitar submenús completos
        self.menu_bar.new_menu.setEnabled(not log_open)
        self.menu_bar.open_menu.setEnabled(not log_open)
        # Exportar y cerrar solo si hay log abierto
        self.menu_bar.export_menu.setEnabled(log_open)
        self.menu_bar.log_close_action.setEnabled(log_open)

    def _connect_menu_actions(self) -> None:
        """
        Conecta las señales personalizadas de la barra de menús a los handlers de MainWindow.
        """
        self.menu_bar.exit_requested.connect(self.close)
        self.menu_bar.manual_requested.connect(lambda: show_manual_dialog(self))
        self.menu_bar.about_requested.connect(lambda: show_about_dialog(self))
        self.menu_bar.open_folder_requested.connect(self._open_data_folder)
        self.menu_bar.light_theme_requested.connect(
            lambda: self._on_theme_selected("light")
        )
        self.menu_bar.dark_theme_requested.connect(
            lambda: self._on_theme_selected("dark")
        )
        self.menu_bar.auto_theme_requested.connect(
            lambda: self._on_theme_selected("auto")
        )
        self.menu_bar.lang_es_requested.connect(
            lambda: self.set_language(LanguageValue.ES)
        )
        self.menu_bar.lang_en_requested.connect(
            lambda: self.set_language(LanguageValue.EN)
        )
        self.menu_bar.lang_auto_requested.connect(
            lambda: self.set_language(LanguageValue.AUTO)
        )
        # Nuevos handlers para submenús
        self.menu_bar.log_new_operativo_requested.connect(
            lambda: action_log_new_operativo(self)
        )
        self.menu_bar.log_new_concurso_requested.connect(
            lambda: action_log_new_concurso(self)
        )
        self.menu_bar.log_open_operativo_requested.connect(
            lambda: action_log_open_operativo(self)
        )
        self.menu_bar.log_open_concurso_requested.connect(
            lambda: action_log_open_concurso(self)
        )
        self.menu_bar.log_close_requested.connect(lambda: action_log_close(self))
        self.menu_bar.db_import_pdf_requested.connect(
            lambda: action_db_import_pdf(self)
        )
        self.menu_bar.db_import_excel_requested.connect(
            lambda: action_db_import_excel(self)
        )
        self.menu_bar.db_export_requested.connect(lambda: action_db_export(self))
        self.menu_bar.db_delete_requested.connect(lambda: action_db_delete(self))
        self.menu_bar.db_show_requested.connect(self._show_db_window)
        self.menu_bar.db_backup_action.triggered.connect(self._on_db_backup)
        self.menu_bar.db_restore_action.triggered.connect(self._on_db_restore)
        self.menu_bar.db_import_db_action.triggered.connect(self._on_db_import_db)
        self.menu_bar.set_callsign_action.triggered.connect(self._on_set_callsign)
        self.menu_bar.callsign_saved_mode_action.triggered.connect(
            self._on_callsign_saved_mode
        )
        self.menu_bar.callsign_always_ask_mode_action.triggered.connect(
            self._on_callsign_always_ask_mode
        )
        self.menu_bar.export_txt_action.triggered.connect(
            lambda: action_log_export_txt(self)
        )
        self.menu_bar.export_csv_action.triggered.connect(
            lambda: action_log_export_csv(self)
        )
        self.menu_bar.export_adi_action.triggered.connect(
            lambda: action_log_export_adi(self)
        )
        self.menu_bar.export_pdf_action.triggered.connect(
            lambda: action_log_export_pdf(self)
        )
        self.menu_bar.export_whatsapp_action.triggered.connect(
            lambda: action_log_export_simple_text(self)
        )

    def _on_theme_selected(self, theme_key: str):
        from .main_window_config import (
            set_light_theme,
            set_dark_theme,
            set_auto_theme,
            update_theme_menu_checks,
        )

        if theme_key == "light":
            set_light_theme(self)
        elif theme_key == "dark":
            set_dark_theme(self)
        elif theme_key == "auto":
            set_auto_theme(self)
        update_theme_menu_checks(self)

    # --- Gestión de base de datos (delegación a acciones) ---
    def _on_db_backup(self):
        action_db_backup(self)

    def _on_db_restore(self):
        action_db_restore(self)

    def _on_db_import_db(self):
        action_db_import_db(self)

    def _open_data_folder(self) -> None:
        action_open_data_folder(self)

    def _show_db_window(self):
        action_show_db_window(self)

    def _on_db_table_window_closed(self, *args):
        action_on_db_table_window_closed(self, *args)

    # --- Eventos y utilidades ---
    def center(self):
        """
        Centra la ventana en la pantalla principal.
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def closeEvent(self, event):
        """
        Evento de cierre de la ventana principal. Cierra la ventana de tabla de base de datos si está abierta.
        """
        if self.db_table_window is not None:
            self.db_table_window.close()
        if hasattr(self, "manual_window") and self.manual_window is not None:
            self.manual_window.close()
        super().closeEvent(event)

    def _on_language_changed(self):
        """
        Handler para el cambio de idioma. Actualiza la UI de la vista activa.
        """
        if self.current_log_type == LogType.CONTEST_LOG:
            self.log_contest_view.retranslate_ui()
        elif self.current_log_type == LogType.OPERATION_LOG:
            self.log_ops_view.retranslate_ui()

    def _on_set_callsign(self):
        """Muestra un diálogo para ingresar el indicativo y lo guarda con persistencia."""
        from PySide6.QtWidgets import QInputDialog

        current_callsign = str(settings_service.get_callsign())
        dialog = QInputDialog(self)
        dialog.setWindowTitle(translation_service.tr("set_callsign_dialog_title"))
        dialog.setLabelText(translation_service.tr("set_callsign_dialog_label"))
        dialog.setTextValue(current_callsign)
        dialog.setMinimumWidth(350)
        dialog.setMinimumHeight(150)

        # Normalización en tiempo real
        def normalize_text(text):
            normalized = text.upper()
            if text != normalized:
                dialog.setTextValue(normalized)

        dialog.textValueChanged.connect(normalize_text)
        ok = dialog.exec()
        callsign = dialog.textValue().upper()
        if ok and callsign:
            settings_service.set_callsign(callsign)
            self._update_callsign_display()

    def _on_callsign_saved_mode(self):
        """Activa el modo 'saved' y actualiza la persistencia y la UI."""
        settings_service.set_callsign_mode(CallsignMode.SAVED)
        self.menu_bar.callsign_saved_mode_action.setChecked(True)
        self.menu_bar.callsign_always_ask_mode_action.setChecked(False)
        self._update_callsign_display()

    def _on_callsign_always_ask_mode(self):
        """Activa el modo 'always_ask' y actualiza la persistencia y la UI."""
        settings_service.set_callsign_mode(CallsignMode.ALWAYS_ASK)
        self.menu_bar.callsign_saved_mode_action.setChecked(False)
        self.menu_bar.callsign_always_ask_mode_action.setChecked(True)
        self._update_callsign_display()

    def _update_callsign_display(self):
        """Actualiza la acción de display para mostrar el indicativo guardado si corresponde."""
        mode = settings_service.get_callsign_mode()
        callsign = settings_service.get_callsign()
        if mode == CallsignMode.SAVED:
            self.menu_bar.callsign_display_action.setText(
                self.tr(f"Saved callsign: {callsign}")
            )
            self.menu_bar.callsign_display_action.setVisible(True)
        else:
            self.menu_bar.callsign_display_action.setText("")
            self.menu_bar.callsign_display_action.setVisible(False)

    def _set_initial_callsign_menu_state(self):
        """Inicializa el estado del submenú Indicative al iniciar la app."""
        mode = settings_service.get_callsign_mode()
        self.menu_bar.callsign_saved_mode_action.setChecked(mode == CallsignMode.SAVED)
        self.menu_bar.callsign_always_ask_mode_action.setChecked(
            mode == CallsignMode.ALWAYS_ASK
        )
        self._update_callsign_display()


# Fin de main_window.py
