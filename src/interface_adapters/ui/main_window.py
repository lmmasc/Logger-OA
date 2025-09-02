from ..core.config.settings_service import settings_service
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QStackedWidget,
    QFileDialog,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
import os
from ..core.config.paths import get_db_path
from .menu_bar import MainMenuBar
from .themes.theme_manager import ThemeManager
from ..core.translation.translation_service import translation_service
from .views.welcome_view import WelcomeView
from .views.log_ops_view import LogOpsView
from .views.log_contest_view import LogContestView
from .view_manager import ViewManager
from application.use_cases.update_operators_from_pdf import update_operators_from_pdf

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
        self.view_manager.register_view("welcome", WelcomeView(self))
        self.view_manager.register_view("log_ops", LogOpsView(self))
        self.view_manager.register_view("log_contest", LogContestView(self))
        self.setCentralWidget(self.view_manager.get_widget())
        self.view_manager.show_view("welcome")

        # Conectar acciones del menú de forma explícita
        self._connect_menu_actions()

        self._menu_action_map = {
            "ops_new": self._action_ops_new,
            "ops_open": self._action_ops_open,
            "ops_export": self._action_ops_export,
            "ops_close": self._action_ops_close,
            "contest_new": self._action_contest_new,
            "contest_open": self._action_contest_open,
            "contest_export": self._action_contest_export,
            "contest_close": self._action_contest_close,
            "db_import_pdf": self._action_db_import_pdf,
            "db_export": self._action_db_export,
        }

        # --- CORRECCIONES Y MEJORAS ---
        # 1. show_view debe ser método de instancia (faltaba tras refactor)
        # 2. Al iniciar, actualizar checks de tema e idioma según configuración guardada
        # Llama este método al final del __init__
        self._set_initial_theme_and_language()

    # =====================
    # Métodos públicos principales
    # =====================

    def show_view(self, view_name: str) -> None:
        """
        Cambia la vista central según el nombre dado usando el gestor de vistas.

        Args:
                view_name (str): Nombre de la vista a mostrar.
        """
        self.view_manager.show_view(view_name)

    def refresh_ui(self) -> None:
        """
        Refresca todos los textos y checks de la interfaz gráfica según el idioma y tema actual.
        Llama a este método tras cambiar idioma o tema para garantizar consistencia visual.
        """
        self.setWindowTitle(translation_service.tr("main_window_title"))
        if hasattr(self.menu_bar, "retranslate_ui"):
            self.menu_bar.retranslate_ui()
        for view in self.view_manager.views.values():
            if hasattr(view, "retranslate_ui"):
                view.retranslate_ui()
        self._update_language_menu_checks()
        self._update_theme_menu_checks()

    # =====================
    # Métodos de configuración y actualización de UI
    # =====================

    def set_language(self, lang: str) -> None:
        """
        Cambia el idioma de la aplicación, lo guarda en la configuración y actualiza los textos de la interfaz.

        Args:
                lang (str): Código del idioma a establecer ("es" o "en").
        """
        translation_service.set_language(lang)
        settings_service.set_value("language", lang)
        self.refresh_ui()

    def set_light_theme(self) -> None:
        """
        Aplica el tema claro a la aplicación y actualiza la interfaz.
        """
        self.theme_manager.apply_theme("light")
        self.refresh_ui()

    def set_dark_theme(self) -> None:
        """
        Aplica el tema oscuro a la aplicación y actualiza la interfaz.
        """
        self.theme_manager.apply_theme("dark")
        self.refresh_ui()

    def _update_theme_menu_checks(self) -> None:
        """
        Actualiza el estado (checked) de las acciones del menú de temas según el tema actual.
        """
        theme = self.theme_manager.current_theme
        self.menu_bar.light_theme_action.setChecked(theme == "light")
        self.menu_bar.dark_theme_action.setChecked(theme == "dark")

    def _update_language_menu_checks(self) -> None:
        """
        Actualiza el estado (checked) de las acciones del menú de idioma según el idioma actual.
        """
        current_lang = translation_service.get_language()
        self.menu_bar.lang_es_action.setChecked(current_lang == "es")
        self.menu_bar.lang_en_action.setChecked(current_lang == "en")

    def _retranslate_ui(self) -> None:
        """
        Actualiza los textos de la interfaz según el idioma seleccionado.
        """
        self.setWindowTitle(translation_service.tr("main_window_title"))
        if hasattr(self.menu_bar, "retranslate_ui"):
            self.menu_bar.retranslate_ui()
        for view in self.view_manager.views.values():
            if hasattr(view, "retranslate_ui"):
                view.retranslate_ui()

    def _set_initial_theme_and_language(self) -> None:
        """
        Aplica el tema y el idioma guardados al iniciar la aplicación.
        """
        theme = self.theme_manager.current_theme
        if theme == "dark":
            self.set_dark_theme()
        else:
            self.set_light_theme()
        lang = settings_service.get_value("language", "es")
        self.set_language(lang)

    # =====================
    # Métodos de conexión de menús y handlers de acciones
    # =====================

    def _connect_menu_actions(self) -> None:
        """
        Conecta las señales personalizadas de la barra de menús a los handlers de MainWindow.
        """
        self.menu_bar.exit_requested.connect(self.close)
        self.menu_bar.about_requested.connect(self.show_about_dialog)
        self.menu_bar.open_folder_requested.connect(self._open_data_folder)
        self.menu_bar.light_theme_requested.connect(self.set_light_theme)
        self.menu_bar.dark_theme_requested.connect(self.set_dark_theme)
        self.menu_bar.lang_es_requested.connect(lambda: self.set_language("es"))
        self.menu_bar.lang_en_requested.connect(lambda: self.set_language("en"))
        self.menu_bar.ops_new_requested.connect(lambda: self._on_menu_action("ops_new"))
        self.menu_bar.ops_open_requested.connect(
            lambda: self._on_menu_action("ops_open")
        )
        self.menu_bar.ops_export_requested.connect(
            lambda: self._on_menu_action("ops_export")
        )
        self.menu_bar.ops_close_requested.connect(
            lambda: self._on_menu_action("ops_close")
        )
        self.menu_bar.contest_new_requested.connect(
            lambda: self._on_menu_action("contest_new")
        )
        self.menu_bar.contest_open_requested.connect(
            lambda: self._on_menu_action("contest_open")
        )
        self.menu_bar.contest_export_requested.connect(
            lambda: self._on_menu_action("contest_export")
        )
        self.menu_bar.contest_close_requested.connect(
            lambda: self._on_menu_action("contest_close")
        )
        self.menu_bar.db_import_pdf_requested.connect(
            lambda: self._on_menu_action("db_import_pdf")
        )
        self.menu_bar.db_export_requested.connect(
            lambda: self._on_menu_action("db_export")
        )
        self.menu_bar.db_show_requested.connect(self._show_db_window)

    def _open_data_folder(self) -> None:
        """
        Abre la carpeta donde se guarda la base de datos.
        """
        db_path = get_db_path()
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

    def show_about_dialog(self):
        """
        Muestra un cuadro de diálogo con información sobre la aplicación.
        """

        QMessageBox.information(
            self,
            translation_service.tr("about"),
            translation_service.tr("about_message"),
        )

    def _on_menu_action(self, action: str):
        handler = self._menu_action_map.get(action)
        if handler:
            handler()
        else:
            QMessageBox.warning(
                self, "Acción no implementada", f"No handler for {action}"
            )

    # Handlers de acciones de menú
    def _action_ops_new(self):
        self.show_view("log_ops")

    def _action_ops_open(self):
        self.show_view("log_ops")

    def _action_ops_export(self):
        self.show_view("log_ops")

    def _action_ops_close(self):
        self.show_view("log_ops")

    def _action_contest_new(self):
        self.show_view("log_contest")

    def _action_contest_open(self):
        self.show_view("log_contest")

    def _action_contest_export(self):
        self.show_view("log_contest")

    def _action_contest_close(self):
        self.show_view("log_contest")

    def _action_db_import_pdf(self) -> None:
        """
        Handler para importar operadores desde PDF. Lógica delegada a un servicio externo.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            translation_service.tr("import_from_pdf"),
            "",
            "PDF Files (*.pdf)",
        )
        if file_path:
            try:
                result = update_operators_from_pdf(file_path)
                if result:
                    QMessageBox.information(
                        self,
                        translation_service.tr("main_window_title"),
                        translation_service.tr("import_success"),
                    )
                else:
                    QMessageBox.warning(
                        self,
                        translation_service.tr("main_window_title"),
                        translation_service.tr("import_failed"),
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    f"{translation_service.tr('import_failed')}: {e}",
                )

    def _action_db_export(self):
        # Lógica de exportar base de datos
        pass

    # =====================
    # Métodos de gestión de ventanas secundarias
    # =====================

    def _show_db_window(self):
        """Muestra la ventana de tabla de base de datos como instancia única."""
        try:
            from .dialogs.db_table_window import DBTableWindow

            if self.db_table_window is not None and self.db_table_window.isVisible():
                self.db_table_window.raise_()
                self.db_table_window.activateWindow()
                return
            self.db_table_window = DBTableWindow(self)
            self.db_table_window.setAttribute(Qt.WA_DeleteOnClose)
            self.db_table_window.destroyed.connect(self._on_db_table_window_closed)
            self.db_table_window.show()
        except Exception as e:
            QMessageBox.warning(
                self, translation_service.tr("main_window_title"), str(e)
            )

    def _on_db_table_window_closed(self, *args):
        self.db_table_window = None

    def closeEvent(self, event):
        # Cerrar la ventana de tabla de base de datos si está abierta
        if self.db_table_window is not None:
            self.db_table_window.close()
        super().closeEvent(event)
