from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
from utils.text import normalize_callsign


class EnterCallsignDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("enter_callsign"))
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        label = QLabel(translation_service.tr("enter_callsign_label"))
        layout.addWidget(label)
        self.callsign_edit = QLineEdit(self)
        self.callsign_edit.setFixedWidth(180)
        layout.addWidget(self.callsign_edit, alignment=Qt.AlignHCenter)
        self.ok_btn = QPushButton(translation_service.tr("ok_button"), self)
        self.ok_btn.setFixedWidth(200)
        layout.addWidget(self.ok_btn, alignment=Qt.AlignHCenter)
        self.callsign = None
        self.ok_btn.clicked.connect(self.set_callsign)
        self.callsign_edit.textChanged.connect(self.normalize_input)

    def set_callsign(self):
        self.callsign = normalize_callsign(self.callsign_edit.text().strip())
        self.accept()

    def normalize_input(self):
        text = self.callsign_edit.text()
        normalized = normalize_callsign(text)
        if text != normalized:
            self.callsign_edit.blockSignals(True)
            self.callsign_edit.setText(normalized)
            self.callsign_edit.blockSignals(False)
