from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
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
        main_layout = QHBoxLayout(self)
        left_box = QVBoxLayout()
        left_box.setContentsMargins(0, 0, 0, 0)
        left_box.setSpacing(0)
        left_box.setAlignment(Qt.AlignTop)
        self.label = QLabel("", self)
        self.input = QLineEdit(self)
        font = QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.input.setFont(font)
        self.input.setMinimumWidth(200)
        self.label.setFixedHeight(32)
        self.input.setFixedHeight(64)
        left_box.addWidget(self.label)
        left_box.addWidget(self.input)
        left_widget = QWidget(self)
        left_widget.setLayout(left_box)
        left_widget.setMinimumWidth(200)
        main_layout.addWidget(left_widget, 2)
        self.setLayout(main_layout)
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
