"""
CallsignInputWidget: Widget para ingreso y normalización de indicativo (callsign).
- Permite validación, autocompletado y adaptación a idioma.
- Señal para agregar a la cola de contactos.
"""

from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel
from PySide6.QtGui import QFont, QFontDatabase
from utils.resources import get_resource_path
from PySide6.QtCore import Signal, Qt
from translation.translation_service import translation_service


class CallsignInputWidget(QWidget):
    addContactRequested = Signal(str)  # Señal para agregar contacto directamente
    """
    Widget independiente para el campo de indicativo (callsign).
    Permite reutilización y fácil integración de validaciones/autocompletado.
    """

    addToQueue = Signal(str)  # Señal para agregar a la cola

    def __init__(self, parent=None):
        """
        Inicializa el widget de ingreso de indicativo.
        Args:
            parent (QWidget): Widget padre.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Label descriptivo
        self.label = QLabel("", self)
        label_font = QFont()
        label_font.setPointSize(14)
        self.label.setFont(label_font)
        # Campo de texto para indicativo
        self.input = QLineEdit(self)
        self.input.setObjectName("callsignInput")
        font_path = get_resource_path("assets/RobotoMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont()
        if font_families:
            font.setFamily(font_families[0])
        else:
            font.setFamily("Monospace")
        font.setPointSize(32)
        font.setBold(True)
        self.input.setFont(font)
        self.input.setFixedWidth(360)
        self.input.setFixedHeight(90)
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        self.setLayout(layout)
        # Conexiones
        self.input.textChanged.connect(self._normalize_upper)
        self.input.installEventFilter(self)
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        # Refuerzo de tabulación: solo el campo input debe recibir el foco
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.retranslate_ui()

    def _normalize_upper(self, text):
        """
        Normaliza el texto a mayúsculas y elimina espacios en tiempo real, manteniendo la posición del cursor.
        Args:
            text (str): Texto ingresado.
        """
        normalized_text = text.replace(" ", "").upper()
        if text != normalized_text:
            cursor_pos = self.input.cursorPosition()
            self.input.blockSignals(True)
            self.input.setText(normalized_text)
            self.input.setCursorPosition(
                cursor_pos
                if cursor_pos <= len(normalized_text)
                else len(normalized_text)
            )
            self.input.blockSignals(False)

    def eventFilter(self, obj, event):
        from PySide6.QtCore import QEvent, Qt

        if obj == self.input and event.type() == QEvent.KeyPress:  # type: ignore
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):  # type: ignore
                text = self.input.text().strip()
                if text:
                    if (
                        event.modifiers() & Qt.KeyboardModifier.ControlModifier
                    ):  # Ctrl+Enter
                        self.addContactRequested.emit(text)
                        return True
                    else:
                        self.addToQueue.emit(text)
                        self.input.clear()
                        return True
        return super().eventFilter(obj, event)

    def get_callsign(self):
        """
        Devuelve el indicativo actual ingresado.
        Returns:
            str: Indicativo en el campo de texto.
        """
        return self.input.text()

    def set_callsign(self, value):
        """
        Establece el indicativo en el campo de texto, normalizado a mayúsculas.
        Args:
            value (str): Indicativo a establecer.
        """
        self.input.setText(value.upper())

    def retranslate_ui(self):
        """
        Actualiza el label según el idioma actual.
        """
        self.label.setText(translation_service.tr("enter_callsign_label"))
