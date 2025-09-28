"""
Archivo principal de la aplicación Logger OA v2.

Este script inicializa la base de datos y lanza la ventana principal usando PySide6.

Flujo principal:
1. Inicializa la base de datos de radioaficionados.
2. Crea la instancia QApplication.
3. Muestra la ventana principal.
4. Maneja cualquier excepción global mostrando un mensaje crítico.
"""

import sys
import traceback

# Terceros
from PySide6.QtWidgets import QApplication, QMessageBox

# Locales
from config.paths import get_database_path
from infrastructure.db.connection import get_connection
from infrastructure.db.schema import init_radioamateur_table
from interface_adapters.ui.main_window import MainWindow
from infrastructure.db import queries


def main():
    """
    Punto de entrada de la aplicación.

    Inicializa la base de datos y lanza la ventana principal.
    Si ocurre una excepción no capturada, muestra un mensaje crítico al usuario.
    """
    try:
        # Inicializar la tabla de radioaficionados en la base de datos usando context manager
        with get_connection(get_database_path()) as conn:
            init_radioamateur_table(conn)

        # Crear la aplicación Qt y mostrar la ventana principal
        app = QApplication(sys.argv)

        # Chequeo automático de vencimientos al arranque
        try:
            affected = queries.disable_expired_operators()
            # Opcional: podríamos registrar 'affected' en el futuro
        except Exception:
            # No bloquear el arranque por este mantenimiento
            pass

        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        # Manejo global de excepciones: muestra mensaje crítico y termina
        app = QApplication.instance() or QApplication(sys.argv)
        error_msg = (
            f"Ocurrió un error inesperado:\n{str(e)}\n\n{traceback.format_exc()}"
        )
        QMessageBox.critical(None, "Error crítico", error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
