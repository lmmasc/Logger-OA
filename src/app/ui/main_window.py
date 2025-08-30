"""
Módulo de la ventana principal de la aplicación.

Contiene la clase MainWindow, que define la ventana principal usando PySide6.
"""

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QStackedWidget

# Importaciones locales
from app.ui.menu_bar import MainMenuBar
from app.ui.themes.theme_manager import ThemeManager
from app.translation import tr, set_language, get_language


from app.ui.views.welcome_view import WelcomeView
from app.ui.views.log_ops_view import LogOpsView
from app.ui.views.log_contest_view import LogContestView


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
        self.setWindowTitle(tr("main_window_title"))  # Título de la ventana
        self.resize(600, 400)  # Solo tamaño inicial
        self.center()

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
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        import os
        from app.utils.file_manager import get_db_path

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
        QMessageBox.information(self, tr("about"), tr("about_message"))

    def set_language(self, lang):
        """
        Cambia el idioma de la aplicación y actualiza los textos de la interfaz.

        Args:
            lang (str): Código del idioma a establecer ("es" o "en").
        """
        set_language(lang)
        self._retranslate_ui()
        self._update_language_menu_checks()

    def _update_language_menu_checks(self):
        """
        Actualiza el estado (checked) de las acciones del menú de idioma según el idioma actual.
        """
        current_lang = get_language()
        self.menu_bar.lang_es_action.setChecked(current_lang == "es")
        self.menu_bar.lang_en_action.setChecked(current_lang == "en")

    def _retranslate_ui(self):
        """
        Actualiza los textos de la interfaz según el idioma seleccionado.
        """
        self.setWindowTitle(tr("main_window_title"))
        from app.translation import retranslate_menu_bar

        retranslate_menu_bar(self.menu_bar)
        # Actualizar todas las vistas que tengan retranslate_ui
        for view in self.views.values():
            if hasattr(view, "retranslate_ui"):
                view.retranslate_ui()

    # Handlers básicos de acciones de menú (placeholders con mensajes)
    def _on_menu_action(self, action: str):
        """
        Cambia la vista central según el menú seleccionado. Preparado para integración futura.
        """
        try:
            if action.startswith("ops_"):
                self.show_view("log_ops")
            elif action.startswith("contest_"):
                self.show_view("log_contest")
            # Aquí puedes agregar más lógica según el tipo de acción
        except Exception as e:
            QMessageBox.information(self, tr("main_window_title"), f"{action}: {e}")

    def _show_db_window(self):
        """Muestra la ventana de tabla de base de datos (placeholder)."""
        try:
            from app.ui.dialogs.db_table_window import DBTableWindow

            dlg = DBTableWindow(self)
            dlg.exec()
        except Exception as e:
            QMessageBox.warning(self, tr("main_window_title"), str(e))
