"""
Archivo principal de la aplicación.

Este script crea y muestra la ventana principal usando PySide6.

- Se importa sys para pasar los argumentos de línea de comandos a QApplication.
- Se importa MainWindow desde app.ui.main_window.
"""

import sys  # Para acceder a los argumentos de línea de comandos
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from infrastructure.db.connection import get_connection
from infrastructure.db.schema import init_radioamateur_table
from app.core.config.paths import get_db_path


def main():
    """Punto de entrada de la aplicación."""
    # Inicializar la tabla de radioaficionados
    conn = get_connection(get_db_path())
    init_radioamateur_table(conn)
    conn.close()

    app = QApplication(
        sys.argv
    )  # QApplication procesa los argumentos de línea de comandos
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # Ejecuta el bucle principal de la aplicación


if __name__ == "__main__":
    main()
