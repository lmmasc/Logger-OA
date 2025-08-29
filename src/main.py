"""
Archivo principal de la aplicación.

Este script crea y muestra la ventana principal usando PySide6.

- Se importa sys para pasar los argumentos de línea de comandos a QApplication.
- Se importa MainWindow desde app.ui.main_window.
"""

import sys  # Para acceder a los argumentos de línea de comandos
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main():
    """Punto de entrada de la aplicación."""
    app = QApplication(
        sys.argv
    )  # QApplication procesa los argumentos de línea de comandos
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # Ejecuta el bucle principal de la aplicación


if __name__ == "__main__":
    main()
