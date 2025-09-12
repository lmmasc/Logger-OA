from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class HeaderWidget(QWidget):
    """
    Widget de encabezado reutilizable para mostrar texto centrado y estilizado en la interfaz.
    Permite actualizar el texto dinámicamente.
    """

    def __init__(self, text="", parent=None):
        """
        Inicializa el widget de encabezado.
        Args:
            text (str): Texto a mostrar en el encabezado.
            parent (QWidget, opcional): Widget padre.
        """
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_text(self, text):
        """
        Actualiza el texto mostrado en el encabezado.
        Args:
            text (str): Nuevo texto para el encabezado.
        """
        self.label.setText(text)
