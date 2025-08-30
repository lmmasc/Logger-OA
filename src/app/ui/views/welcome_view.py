from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from app.translation import tr
from app.translation.translation_events import translation_signal


class WelcomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel(tr("welcome_message"))
        layout.addWidget(self.label)
        self.setLayout(layout)
        translation_signal.language_changed.connect(self.retranslate_ui)

    def retranslate_ui(self):
        self.label.setText(tr("welcome_message"))
