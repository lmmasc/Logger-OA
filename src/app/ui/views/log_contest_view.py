from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from app.translation import tr


class LogContestView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel(tr("log_contest"))
        layout.addWidget(label)
        self.setLayout(layout)
