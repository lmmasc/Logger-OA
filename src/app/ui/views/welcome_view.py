from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from app.ui.translations import tr


class WelcomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel(tr("welcome_message"))
        layout.addWidget(label)
        self.setLayout(layout)
