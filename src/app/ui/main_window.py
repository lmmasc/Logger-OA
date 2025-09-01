from app.core.config.settings_service import settings_service
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
from app.core.config.paths import get_db_path
from app.ui.menu_bar import MainMenuBar
from app.ui.themes.theme_manager import ThemeManager
from app.core.translation.translation_service import translation_service
from app.ui.views.welcome_view import WelcomeView
from app.ui.views.log_ops_view import LogOpsView
from app.ui.views.log_contest_view import LogContestView


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

        # --- Vistas dinámicas ---
        self.stacked_widget = QStackedWidget()
        self.views = {
            "welcome": WelcomeView(self),
            "log_ops": LogOpsView(self),
            "log_contest": LogContestView(self),
        }
        for view in self.views.values():
            self.stacked_widget.addWidget(view)
        self.setCentralWidget(self.stacked_widget)
        self.show_view("welcome")

    def show_view(self, view_name):
        """
        Cambia la vista central según el nombre dado.
        """
        view = self.views.get(view_name)
        if view:
            self.stacked_widget.setCurrentWidget(view)

        # Conectar acciones del menú de forma explícita
        self.menu_bar.exit_action.triggered.connect(self.close)
        self.menu_bar.about_action.triggered.connect(self.show_about_dialog)

        # Acción para abrir carpeta de archivos
        def open_data_folder():
            # Carpeta donde se guarda la base de datos
            db_path = get_db_path()
            folder = os.path.dirname(db_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

        self.menu_bar.open_folder_action.triggered.connect(open_data_folder)

        # Acciones de tema
        self.menu_bar.light_theme_action.triggered.connect(self.set_light_theme)
        self.menu_bar.dark_theme_action.triggered.connect(self.set_dark_theme)

        # Acciones de idioma
        self.menu_bar.lang_es_action.triggered.connect(lambda: self.set_language("es"))
        self.menu_bar.lang_en_action.triggered.connect(lambda: self.set_language("en"))

        self._update_language_menu_checks()
        self._update_theme_menu_checks()

        # Conectar menús Operativo y Concurso
        # Nota: las funciones concretas pueden integrarse con vistas específicas más adelante.
        self.menu_bar.ops_new_action.triggered.connect(
            lambda: self._on_menu_action("ops_new")
        )
        self.menu_bar.ops_open_action.triggered.connect(
            lambda: self._on_menu_action("ops_open")
        )
        self.menu_bar.ops_export_action.triggered.connect(
            lambda: self._on_menu_action("ops_export")
        )
        self.menu_bar.ops_close_action.triggered.connect(
            lambda: self._on_menu_action("ops_close")
        )

        self.menu_bar.contest_new_action.triggered.connect(
            lambda: self._on_menu_action("contest_new")
        )
        self.menu_bar.contest_open_action.triggered.connect(
            lambda: self._on_menu_action("contest_open")
        )
        self.menu_bar.contest_export_action.triggered.connect(
            lambda: self._on_menu_action("contest_export")
        )
        self.menu_bar.contest_close_action.triggered.connect(
            lambda: self._on_menu_action("contest_close")
        )

        # Conectar menú Base de datos
        self.menu_bar.db_import_pdf_action.triggered.connect(
            lambda: self._on_menu_action("db_import_pdf")
        )
        self.menu_bar.db_export_action.triggered.connect(
            lambda: self._on_menu_action("db_export")
        )
        self.menu_bar.db_show_action.triggered.connect(self._show_db_window)

    def center(self):
        """
        Centra la ventana en la pantalla principal.
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def set_light_theme(self):
        """
        Aplica el tema claro a la aplicación y actualiza el estado del menú de temas.
        """
        self.theme_manager.apply_theme("light")
        self._update_theme_menu_checks()

    def set_dark_theme(self):
        """
        Aplica el tema oscuro a la aplicación y actualiza el estado del menú de temas.
        """
        self.theme_manager.apply_theme("dark")
        self._update_theme_menu_checks()

    def _update_theme_menu_checks(self):
        """
        Actualiza el estado (checked) de las acciones del menú de temas según el tema actual.
        """
        theme = self.theme_manager.current_theme
        self.menu_bar.light_theme_action.setChecked(theme == "light")
        self.menu_bar.dark_theme_action.setChecked(theme == "dark")

    def show_about_dialog(self):
        """
        Muestra un cuadro de diálogo con información sobre la aplicación.
        """

        QMessageBox.information(
            self,
            translation_service.tr("about"),
            translation_service.tr("about_message"),
        )

    def set_language(self, lang):
        """
        Cambia el idioma de la aplicación, lo guarda en la configuración y actualiza los textos de la interfaz.

        Args:
            lang (str): Código del idioma a establecer ("es" o "en").
        """
        translation_service.set_language(lang)
        settings_service.set_value("language", lang)
        self._retranslate_ui()
        self._update_language_menu_checks()

    def _update_language_menu_checks(self):
        """
        Actualiza el estado (checked) de las acciones del menú de idioma según el idioma actual.
        """
        current_lang = translation_service.get_language()
        self.menu_bar.lang_es_action.setChecked(current_lang == "es")
        self.menu_bar.lang_en_action.setChecked(current_lang == "en")

    def _retranslate_ui(self):
        """
        Actualiza los textos de la interfaz según el idioma seleccionado.
        """
        self.setWindowTitle(translation_service.tr("main_window_title"))
        if hasattr(self.menu_bar, "retranslate_ui"):
            self.menu_bar.retranslate_ui()
        # Actualizar todas las vistas que tengan retranslate_ui
        for view in self.views.values():
            if hasattr(view, "retranslate_ui"):
                view.retranslate_ui()

    # Handlers básicos de acciones de menú (placeholders con mensajes)
    def _on_menu_action(self, action: str):
        """
        Maneja acciones de menú, incluyendo importación de operadores desde PDF.
        """
        try:
            if action.startswith("ops_"):
                self.show_view("log_ops")
            elif action.startswith("contest_"):
                self.show_view("log_contest")
            elif action == "db_import_pdf":
                from app.operators_update.updater import update_operators_from_pdf

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
        except Exception as e:
            QMessageBox.information(
                self, translation_service.tr("main_window_title"), f"{action}: {e}"
            )

    def _show_db_window(self):
        """Muestra la ventana de tabla de base de datos como instancia única."""
        try:
            from app.ui.dialogs.db_table_window import DBTableWindow

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
