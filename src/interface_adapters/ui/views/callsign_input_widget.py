from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, Qt
from translation.translation_service import translation_service


class CallsignInputWidget(QWidget):
    """
    Widget independiente para el campo de indicativo (callsign).
    Permite reutilización y fácil integración de validaciones/autocompletado.
    """

    addToQueue = Signal(str)  # Señal para agregar a la cola

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        self.label = QLabel("", self)
        label_font = QFont()
        label_font.setPointSize(14)
        label_font.setBold(True)
        self.label.setFont(label_font)
        self.input = QLineEdit(self)
        font = QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.input.setFont(font)
        # self.input.setMinimumWidth(200)
        # self.input.setMaximumWidth(200)
        self.input.setFixedWidth(320)
        # self.label.setFixedHeight(32)
        self.input.setFixedHeight(64)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        self.setLayout(layout)
        self.input.textChanged.connect(self._normalize_upper)
        self.retranslate_ui()
        self.input.returnPressed.connect(self._on_return_pressed)

    def _normalize_upper(self, text):
        upper_text = text.upper()
        if text != upper_text:
            cursor_pos = self.input.cursorPosition()
            self.input.blockSignals(True)
            self.input.setText(upper_text)
            self.input.setCursorPosition(cursor_pos)
            self.input.blockSignals(False)

    def get_callsign(self):
        return self.input.text()

    def set_callsign(self, value):
        self.input.setText(value.upper())

    def _on_return_pressed(self):
        text = self.input.text().strip()
        if text:
            self.addToQueue.emit(text)
            self.input.clear()

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("enter_callsign_label"))
