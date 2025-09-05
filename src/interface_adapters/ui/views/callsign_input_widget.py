from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel
from translation.translation_service import translation_service


class CallsignInputWidget(QWidget):
    """
    Widget independiente para el campo de indicativo (callsign).
    Permite reutilización y fácil integración de validaciones/autocompletado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(translation_service.tr("callsign"), self)
        self.input = QLineEdit(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        self.setLayout(layout)

    def get_callsign(self):
        return self.input.text()

    def set_callsign(self, value):
        self.input.setText(value)

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("callsign"))
