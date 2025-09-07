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
        self.label = QLabel(translation_service.tr("callsign"), self)
        self.input = QLineEdit(self)
        font = QFont()
        font.setPointSize(32)  # Fuente mucho más grande
        font.setBold(True)
        self.input.setFont(font)
        left_box.addWidget(self.label)
        left_box.addWidget(self.input)
        left_widget = QWidget(self)
        left_widget.setLayout(left_box)
        left_widget.setMinimumWidth(120)
        left_widget.setMaximumWidth(400)
        main_layout.addWidget(left_widget, 1)
        # Sección derecha: resumen

        self.summary_box = QGroupBox(translation_service.tr("callsign_summary"), self)
        self.summary_label = QLabel("", self.summary_box)
        summary_font = QFont()
        summary_font.setPointSize(20)  # Fuente aún más grande para el resumen
        self.summary_label.setFont(summary_font)
        summary_layout = QVBoxLayout(self.summary_box)
        summary_layout.addWidget(self.summary_label)
        self.summary_box.setLayout(summary_layout)
        main_layout.addWidget(self.summary_box, 3)
        self.setLayout(main_layout)

    def get_callsign(self):
        return self.input.text()

    def set_callsign(self, value):
        self.input.setText(value)

    def set_summary(self, text):
        self.summary_label.setText(text)
        self.summary_label.setMinimumHeight(
            80
        )  # Altura mínima para evitar redimensionamiento
        summary_font = QFont()
        summary_font.setPointSize(20)  # Mantener fuente grande en cada actualización
        self.summary_label.setFont(summary_font)

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("callsign"))
        self.summary_box.setTitle(translation_service.tr("callsign_summary"))
        # Retraducir el resumen si existe
        if self.summary_label.text():
            self.set_summary(self.summary_label.text())
