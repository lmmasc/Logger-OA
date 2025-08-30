"""
Módulo de la ventana principal de la aplicación.

Contiene la clase MainWindow, que define la ventana principal usando PySide6.
"""

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from app.ui.menu_bar import MainMenuBar
from app.ui.themes.theme_manager import ThemeManager
from app.ui.translations import tr


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    Hereda de QMainWindow y configura el título y tamaño inicial.
    La ventana aparece centrada en la pantalla.
    """

    def __init__(self):
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

        # Conectar acciones del menú de forma explícita
        self.menu_bar.exit_action.triggered.connect(self.close)
        self.menu_bar.about_action.triggered.connect(self.show_about_dialog)

        # Acciones de tema
        self.menu_bar.light_theme_action.triggered.connect(self.set_light_theme)
        self.menu_bar.dark_theme_action.triggered.connect(self.set_dark_theme)

        # Acciones de idioma
        self.menu_bar.lang_es_action.triggered.connect(lambda: self.set_language("es"))
        self.menu_bar.lang_en_action.triggered.connect(lambda: self.set_language("en"))
        self._update_language_menu_checks()

        self._update_theme_menu_checks()

    def set_light_theme(self):
        self.theme_manager.apply_theme("light")
        self._update_theme_menu_checks()

    def set_dark_theme(self):
        self.theme_manager.apply_theme("dark")
        self._update_theme_menu_checks()

    def _update_theme_menu_checks(self):
        theme = self.theme_manager.current_theme
        self.menu_bar.light_theme_action.setChecked(theme == "light")
        self.menu_bar.dark_theme_action.setChecked(theme == "dark")

    def show_about_dialog(self):
        QMessageBox.information(self, tr("about"), tr("about_message"))

    def center(self):
        """Centra la ventana en la pantalla principal."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def set_language(self, lang):
        from app.ui.translations import set_language, tr

        set_language(lang)
        self._retranslate_ui()
        self._update_language_menu_checks()

    def _update_language_menu_checks(self):
        from app.ui.translations import current_lang

        self.menu_bar.lang_es_action.setChecked(current_lang == "es")
        self.menu_bar.lang_en_action.setChecked(current_lang == "en")

    def _retranslate_ui(self):
        from app.ui.translations import tr

        self.setWindowTitle(tr("main_window_title"))
        # Menús y acciones
        self.menu_bar.actions()[0].menu().setTitle(tr("file_menu"))
        self.menu_bar.exit_action.setText(tr("exit"))
        self.menu_bar.actions()[1].menu().setTitle(tr("aspect_menu"))
        self.menu_bar.light_theme_action.setText(tr("light_theme"))
        self.menu_bar.dark_theme_action.setText(tr("dark_theme"))
        self.menu_bar.actions()[2].menu().setTitle(tr("help_menu"))
        self.menu_bar.about_action.setText(tr("about"))
        self.menu_bar.actions()[3].menu().setTitle(tr("language_menu"))
        self.menu_bar.lang_es_action.setText(tr("spanish"))
        self.menu_bar.lang_en_action.setText(tr("english"))
