from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from app.core.translation.translation_service import translation_service


class LogOpsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel(translation_service.tr("log_ops"))
        layout.addWidget(self.label)
        self.setLayout(layout)

        translation_service.signal.language_changed.connect(self.retranslate_ui)

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("log_ops"))
