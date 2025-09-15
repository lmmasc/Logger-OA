"""
WaitDialog
Diálogo de espera para procesos largos.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class WaitDialog(QDialog):
    def __init__(self, parent=None, message=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("main_window_title"))
        self.setModal(True)
        layout = QVBoxLayout(self)
        label = QLabel(message or translation_service.tr("wait_message"))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setFixedSize(300, 100)
