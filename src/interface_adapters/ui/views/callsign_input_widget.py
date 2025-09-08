from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
)
from PySide6.QtGui import QFont
from translation.translation_service import translation_service


class CallsignInputWidget(QWidget):
    """
    Widget independiente para el campo de indicativo (callsign).
    Permite reutilización y fácil integración de validaciones/autocompletado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        # Sección izquierda: label encima del campo
        left_box = QVBoxLayout()
        self.label = QLabel("", self)  # Inicializa vacío para traducir luego
        self.input = QLineEdit(self)
        font = QFont()
        font.setPointSize(32)  # Fuente mucho más grande
        font.setBold(True)
        self.input.setFont(font)
        self.input.setMinimumWidth(200)  # Ajuste leve para evitar recorte
        # Elimina setMaximumWidth en input y contenedor
        left_box.addWidget(self.label)
        left_box.addWidget(self.input)
        left_widget = QWidget(self)
        left_widget.setLayout(left_box)
        left_widget.setMinimumWidth(200)
        main_layout.addWidget(left_widget, 2)  # Stretch factor bajo para indicativo
        # Sección derecha: resumen
        self.summary_box = QGroupBox("", self)
        self.summary_label = QLabel("", self.summary_box)
        summary_font = QFont()
        summary_font.setPointSize(20)
        self.summary_label.setFont(summary_font)
        self.summary_label.setMinimumHeight(80)
        summary_layout = QVBoxLayout(self.summary_box)
        summary_layout.addWidget(self.summary_label)
        self.summary_box.setLayout(summary_layout)
        main_layout.addWidget(self.summary_box, 5)  # Stretch factor alto para resumen
        self.setLayout(main_layout)
        # Normalizar a mayúsculas en tiempo real
        self.input.textChanged.connect(self._normalize_upper)
        # Traducir label y box al crear el widget
        self.retranslate_ui()

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

    def set_summary(self, text):
        self.summary_label.setText(text)

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("callsign"))
        self.summary_box.setTitle(translation_service.tr("callsign_summary"))
        # Retraducir el resumen si existe
        if self.summary_label.text():
            self.set_summary(self.summary_label.text())
