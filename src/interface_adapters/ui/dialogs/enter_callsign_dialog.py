"""
EnterCallsignDialog
Diálogo para ingresar y normalizar un indicativo de operador.
"""

# --- Imports de terceros ---
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

# --- Imports de la aplicación ---
from translation.translation_service import translation_service
from utils.text import normalize_callsign


class EnterCallsignDialog(QDialog):
    """
    Diálogo para ingresar y normalizar un indicativo de operador.
    """

    def __init__(self, parent=None):
        """
        Inicializa el diálogo para ingresar el indicativo.
        Args:
            parent (QWidget, opcional): Widget padre.
        """
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("enter_callsign"))
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        label = QLabel(translation_service.tr("enter_callsign_label"))
        layout.addWidget(label)
        self.callsign_edit = QLineEdit(self)
        self.callsign_edit.setFixedWidth(180)
        layout.addWidget(self.callsign_edit, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.ok_btn = QPushButton(translation_service.tr("ok_button"), self)
        self.ok_btn.setFixedWidth(200)
        layout.addWidget(self.ok_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.callsign = None
        self.ok_btn.clicked.connect(self.set_callsign)
        self.callsign_edit.textChanged.connect(self.normalize_input)

    def set_callsign(self):
        """
        Normaliza y guarda el indicativo ingresado, luego cierra el diálogo.
        """
        self.callsign = normalize_callsign(self.callsign_edit.text().strip())
        self.accept()

    def normalize_input(self):
        """
        Normaliza el texto del campo de indicativo en tiempo real.
        """
        text = self.callsign_edit.text()
        normalized = normalize_callsign(text)
        if text != normalized:
            self.callsign_edit.blockSignals(True)
            self.callsign_edit.setText(normalized)
            self.callsign_edit.blockSignals(False)
