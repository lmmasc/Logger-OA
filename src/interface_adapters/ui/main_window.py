from config.settings_service import settings_service
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QStackedWidget,
    QFileDialog,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QDesktopServices
import os
from config.paths import get_db_path
from .menu_bar import MainMenuBar
from .themes.theme_manager import ThemeManager
from translation.translation_service import translation_service
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
        self.view_manager.register_view("welcome", WelcomeView(self))
        self.view_manager.register_view("log_ops", LogOpsView(self))
        self.view_manager.register_view("log_contest", LogContestView(self))
        self.setCentralWidget(self.view_manager.get_widget())
        self.view_manager.show_view("welcome")

        # Conectar acciones del menú de forma explícita
        self._connect_menu_actions()

        self._menu_action_map = {
            "log_new": self._action_log_new,
            "log_open": self._action_log_open,
            "log_export": self._action_log_export,
            "log_close": self._action_log_close,
            "db_import_pdf": self._action_db_import_pdf,
            "db_export": self._action_db_export,
            "db_delete": self._action_db_delete,
        }

        # --- CORRECCIONES Y MEJORAS ---
        # 1. show_view debe ser método de instancia (faltaba tras refactor)
        # 2. Al iniciar, actualizar checks de tema e idioma según configuración guardada
        # Llama este método al final del __init__
        self._set_initial_theme_and_language()
        self.update_menu_state()  # Estado inicial del menú

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
        if self.db_table_window is not None and hasattr(
            self.db_table_window, "retranslate_ui"
        ):
            self.db_table_window.retranslate_ui()
        self._update_language_menu_checks()
        self._update_theme_menu_checks()

    # =====================
    # Métodos de configuración y actualización de UI
    # =====================

    def set_language(self, lang: str) -> None:
        """
        Cambia el idioma de la aplicación, lo guarda en la configuración y actualiza los textos de la interfaz.
        Solo guarda si el idioma realmente cambió.

        Args:
                lang (str): Código del idioma a establecer ("es" o "en").
        """
        translation_service.set_language(lang)
        current_lang = settings_service.get_value("language", "es")
        if current_lang != lang:
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
        self.menu_bar.about_requested.connect(self.show_about_dialog)
        self.menu_bar.open_folder_requested.connect(self._open_data_folder)
        self.menu_bar.light_theme_requested.connect(self.set_light_theme)
        self.menu_bar.dark_theme_requested.connect(self.set_dark_theme)
        self.menu_bar.lang_es_requested.connect(lambda: self.set_language("es"))
        self.menu_bar.lang_en_requested.connect(lambda: self.set_language("en"))
        self.menu_bar.log_new_requested.connect(lambda: self._on_menu_action("log_new"))
        self.menu_bar.log_open_requested.connect(
            lambda: self._on_menu_action("log_open")
        )
        self.menu_bar.log_export_requested.connect(
            lambda: self._on_menu_action("log_export")
        )
        self.menu_bar.log_close_requested.connect(
            lambda: self._on_menu_action("log_close")
        )
        self.menu_bar.db_import_pdf_requested.connect(
            lambda: self._on_menu_action("db_import_pdf")
        )
        self.menu_bar.db_export_requested.connect(
            lambda: self._on_menu_action("db_export")
        )
        self.menu_bar.db_delete_requested.connect(self._action_db_delete)
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

    # Handler unificado para acciones de log
    def _action_log_new(self):
        """
        Muestra un diálogo para elegir el tipo de log y crea el archivo SQLite usando el módulo de paths y casos de uso.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(translation_service.tr("select_log_type"))
        layout = QVBoxLayout(dialog)
        label = QLabel(translation_service.tr("select_log_type_label"))
        layout.addWidget(label)
        btn_ops = QPushButton(translation_service.tr("log_type_ops"), dialog)
        btn_contest = QPushButton(translation_service.tr("log_type_contest"), dialog)
        layout.addWidget(btn_ops)
        layout.addWidget(btn_contest)
        selected = {"type": None}

        def select_ops():
            selected["type"] = "ops"
            dialog.accept()

        def select_contest():
            selected["type"] = "contest"
            dialog.accept()

        btn_ops.clicked.connect(select_ops)
        btn_contest.clicked.connect(select_contest)
        dialog.exec()
        if selected["type"] in ("ops", "contest"):
            # Aquí integrar lógica para crear y abrir log de operaciones/concurso
            self.current_log = object()  # Simulación de log creado
            self.current_log_type = selected["type"]
            self.show_view(f"log_{self.current_log_type}")
        else:
            self.current_log = None
            self.current_log_type = None
            self.show_view("welcome")
        self.update_menu_state()

    def _action_log_open(self):
        """
        Abre un log existente usando el módulo de paths y casos de uso.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            translation_service.tr("open_log"),
            "",
            "SQLite Files (*.sqlite);;All Files (*)",
        )
        if file_path:
            try:
                from application.use_cases.open_log import open_log

                log = open_log(file_path)
                self.current_log = log
                # Determinar tipo de log por instancia
                if hasattr(
                    log, "__class__"
                ) and log.__class__.__name__.lower().startswith("operation"):
                    self.current_log_type = "ops"
                elif hasattr(
                    log, "__class__"
                ) and log.__class__.__name__.lower().startswith("contest"):
                    self.current_log_type = "contest"
                else:
                    self.current_log_type = None
                if self.current_log_type:
                    self.show_view(f"log_{self.current_log_type}")
                else:
                    self.show_view("welcome")
                    self.current_log = None
            except Exception as e:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    f"{translation_service.tr('open_failed')}: {e}",
                )
                self.current_log = None
                self.current_log_type = None
                self.show_view("welcome")
        else:
            self.current_log = None
            self.current_log_type = None
            self.show_view("welcome")
        self.update_menu_state()

    def _action_log_export(self):
        # Exportar el log actual según el tipo
        current_view = self.view_manager.get_current_view_name()
        if current_view == "log_ops":
            self.show_view("log_ops")
        elif current_view == "log_contest":
            self.show_view("log_contest")

    def _action_log_close(self):
        """
        Cierra el log actual y regresa a la vista de bienvenida.
        """
        self.current_log = None
        self.current_log_type = None
        self.show_view("welcome")
        self.update_menu_state()

    def _action_db_import_pdf(self) -> None:
        """
        Handler para importar operadores desde PDF. Muestra spinner y asegura repintado antes del proceso bloqueante.
        """
        from PySide6.QtCore import QTimer

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            translation_service.tr("import_from_pdf"),
            "",
            "PDF Files (*.pdf)",
        )
        if file_path:
            wait_dialog = QDialog(self)
            wait_dialog.setWindowTitle(translation_service.tr("main_window_title"))
            wait_dialog.setModal(True)
            layout = QVBoxLayout(wait_dialog)
            label = QLabel(translation_service.tr("wait_message"))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            wait_dialog.setFixedSize(300, 100)
            wait_dialog.show()
            QApplication.processEvents()

            def do_import():
                try:
                    result = update_operators_from_pdf(file_path)
                except Exception as e:
                    wait_dialog.close()
                    QMessageBox.critical(
                        self,
                        translation_service.tr("main_window_title"),
                        f"{translation_service.tr('import_failed')}: {e}",
                    )
                    return
                wait_dialog.close()
                # --- NUEVO: Mostrar resumen si está disponible ---
                if isinstance(result, dict) and result.get("ok"):
                    summary = result
                    summary_lines = [
                        translation_service.tr("import_summary_total").format(
                            summary.get("total", 0)
                        ),
                        translation_service.tr("import_summary_new").format(
                            summary.get("new", 0)
                        ),
                        translation_service.tr("import_summary_updated").format(
                            summary.get("updated", 0)
                        ),
                        translation_service.tr("import_summary_unchanged").format(
                            summary.get("unchanged", 0)
                        ),
                        translation_service.tr("import_summary_disabled").format(
                            summary.get("disabled", 0)
                        ),
                        translation_service.tr("import_summary_reenabled").format(
                            summary.get("reenabled", 0)
                        ),
                    ]
                    if "protected" in summary:
                        summary_lines.append(
                            translation_service.tr("import_summary_protected").format(
                                summary["protected"]
                            )
                        )
                    # No mostrar 'ok' en el resumen, ya que solo indica éxito/fallo
                    msg = "<br>".join(summary_lines)
                    QMessageBox.information(
                        self,
                        translation_service.tr("main_window_title"),
                        msg,
                    )
                elif result:
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

            QTimer.singleShot(100, do_import)  # 100 ms para asegurar repintado

    def _action_db_export(self):
        # Lógica de exportar base de datos
        pass

    def _action_db_delete(self):
        """
        Handler para borrar y recrear la base de datos, mostrando advertencia y confirmación.
        """
        from translation.translation_service import translation_service
        from infrastructure.db.reset import reset_database

        yes_text = translation_service.tr("yes_button")
        no_text = translation_service.tr("no_button")
        box = QMessageBox(self)
        box.setWindowTitle(translation_service.tr("delete_db_confirm"))
        box.setText(translation_service.tr("delete_db_warning"))
        yes_button = box.addButton(yes_text, QMessageBox.YesRole)
        no_button = box.addButton(no_text, QMessageBox.NoRole)
        box.setDefaultButton(no_button)
        box.exec()
        if box.clickedButton() == yes_button:
            try:
                reset_database()
                QMessageBox.information(
                    self,
                    translation_service.tr("main_window_title"),
                    translation_service.tr("delete_db_success"),
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    f"{translation_service.tr('import_failed')}: {e}",
                )
        else:
            QMessageBox.information(
                self,
                translation_service.tr("main_window_title"),
                translation_service.tr("delete_db_cancel"),
            )

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
