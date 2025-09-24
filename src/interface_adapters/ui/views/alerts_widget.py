"""
Widget de alertas para Logger OA: muestra dos labels de alerta/información.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class AlertsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label1 = QLabel("Duplicado", self)
        self.label2 = QLabel("Inhabilitado", self)
        self.label1.setObjectName("AlertLabel1")
        self.label2.setObjectName("AlertLabel2")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setFixedHeight(32)
        self.label2.setFixedHeight(32)

        self.label1.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.label2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.label1, 1)
        layout.addWidget(self.label2, 1)
        self.setLayout(layout)
        self.setSizePolicy(self.sizePolicy())
        # Hacer visible el widget aunque esté vacío
        self.setMinimumHeight(48)
        self.setStyleSheet(
            "background: #fffbe6; border: 1px solid #e6c200; border-radius: 4px;"
        )

        self.label1.setStyleSheet("color: #a67c00; font-weight: bold; font-size: 20px;")
        self.label2.setStyleSheet("color: #a67c00; font-weight: bold; font-size: 20px;")

    def set_alerts(self, text1, text2):
        self.label1.setText(text1)
        self.label2.setText(text2)

    def clear_alerts(self):
        self.label1.setText("")
        self.label2.setText("")
