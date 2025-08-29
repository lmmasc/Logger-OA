"""
Módulo de la ventana principal de la aplicación.

Contiene la clase MainWindow, que define la ventana principal usando PySide6.
"""

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from app.ui.menu_bar import MainMenuBar
from app.ui.themes.theme_manager import ThemeManager


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    Hereda de QMainWindow y configura el título y tamaño inicial.
    La ventana aparece centrada en la pantalla.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")  # Título de la ventana
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
        QMessageBox.information(
            self, "Acerca de", "Logger OA v2\nAplicación de ejemplo con PySide6."
        )

    def center(self):
        """Centra la ventana en la pantalla principal."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())
