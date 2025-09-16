"""
WaitDialog

Diálogo de espera para procesos largos.
Muestra un mensaje de espera mientras se ejecuta una tarea en segundo plano.
"""

# --- Imports de terceros ---
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# --- Imports de la aplicación ---
from translation.translation_service import translation_service


class WaitDialog(QDialog):
    """
    Diálogo modal de espera para procesos largos.
    Muestra un mensaje personalizado o el mensaje por defecto traducido.
    """

    def __init__(self, parent=None, message=None):
        """
        Inicializa el diálogo de espera.
        Args:
            parent (QWidget, opcional): Widget padre.
            message (str, opcional): Mensaje a mostrar. Si no se indica, se usa el mensaje traducido por defecto.
        """
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("main_window_title"))
        self.setModal(True)
        layout = QVBoxLayout(self)
        label = QLabel(message or translation_service.tr("wait_message"))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setFixedSize(300, 100)
