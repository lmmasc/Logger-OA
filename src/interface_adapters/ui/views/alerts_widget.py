"""
Widget de alertas para Logger OA: muestra dos labels de alerta/información.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class AlertsWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        from translation.translation_service import translation_service

        self._translation_service = translation_service
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label1 = QLabel(self._translation_service.tr("ui_alert_duplicate"), self)
        self.label2 = QLabel(self._translation_service.tr("ui_alert_disabled"), self)
        self.label1.setObjectName("AlertLabel")
        self.label2.setObjectName("AlertLabel")
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
        # Inicializa tema y estado
        self.label1.setEnabled(False)
        self.label2.setEnabled(False)

        # Suscribirse a cambios de idioma
        self._translation_service.signal.language_changed.connect(
            self._update_translations
        )

    def _update_translations(self):
        self.label1.setText(self._translation_service.tr("ui_alert_duplicate"))
        self.label2.setText(self._translation_service.tr("ui_alert_disabled"))

    def set_duplicate_alert(self, enabled: bool):
        """
        Cambia el estado habilitado/inhabilitado de la alerta de duplicado.
        """
        self.label1.setEnabled(enabled)

    def set_disabled_alert(self, enabled: bool):
        """
        Cambia el estado habilitado/inhabilitado de la alerta de operador deshabilitado.
        """
        self.label2.setEnabled(enabled)

    def clear_alerts(self):
        self.label1.setEnabled(False)
        self.label2.setEnabled(False)
