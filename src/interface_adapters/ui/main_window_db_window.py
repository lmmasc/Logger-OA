"""
Módulo para la gestión de la ventana de base de datos en MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QMessageBox
from translation.translation_service import translation_service


def show_db_window(self):
    """
    Muestra la ventana de tabla de base de datos como instancia única.
    """
    try:
        from .views.db_table_window import DBTableWindow

        if self.db_table_window is not None and self.db_table_window.isVisible():
            self.db_table_window.raise_()
            self.db_table_window.activateWindow()
            return
        self.db_table_window = DBTableWindow(self)
        self.db_table_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db_table_window.destroyed.connect(
            lambda *args: on_db_table_window_closed(self)
        )
        self.db_table_window.show()
    except Exception as e:
        QMessageBox.warning(self, translation_service.tr("main_window_title"), str(e))


def on_db_table_window_closed(self, *args):
    self.db_table_window = None
