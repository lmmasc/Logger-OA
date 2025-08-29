"""
Módulo de la ventana principal de la aplicación.

Contiene la clase MainWindow, que define la ventana principal usando PySide6.
"""

from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from app.ui.menu_bar import MainMenuBar


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

        # Conectar acciones del menú
        self._connect_menu_actions()

    def _connect_menu_actions(self):
        # Buscar acciones por texto
        file_menu = self.menu_bar.findChild(type(self.menu_bar.addMenu("")), "Archivo")
        help_menu = self.menu_bar.findChild(type(self.menu_bar.addMenu("")), "Ayuda")

        # Alternativamente, buscar por orden
        file_menu = self.menu_bar.actions()[0].menu()
        help_menu = self.menu_bar.actions()[1].menu()

        exit_action = file_menu.actions()[0]
        about_action = help_menu.actions()[0]

        exit_action.triggered.connect(self.close)
        about_action.triggered.connect(self.show_about_dialog)

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
