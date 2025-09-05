"""
Módulo de diálogos personalizados para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from PySide6.QtWidgets import QMessageBox
from translation.translation_service import translation_service


def show_about_dialog(self):
    """
    Muestra un cuadro de diálogo con información sobre la aplicación.
    """
    QMessageBox.information(
        self,
        translation_service.tr("about"),
        translation_service.tr("about_message"),
    )


# Si hay otros diálogos puros, se pueden agregar aquí como funciones.
