from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class HeaderWidget(QWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 8px 0;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_text(self, text):
        self.label.setText(text)
