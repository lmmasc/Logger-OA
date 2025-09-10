"""
ClockWidget: Widget de reloj digital con soporte OA/UTC y formato de fecha/hora dependiente de idioma.
- Compatible multiplataforma (fuente monoespaciada).
- Actualiza cada segundo.
- Colores y estilos configurables vía QSS.
"""

import datetime
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class ClockWidget(QWidget):
    """
    Widget de reloj digital para mostrar hora y fecha en formato OA o UTC.
    El formato de fecha depende del idioma configurado en translation_service.
    El color y el estilo se configuran vía QSS usando objectName.
    """

    def __init__(self, label_text, color, parent=None, utc=False):
        """
        Inicializa el widget de reloj.
        Args:
            label_text (str): Texto fijo del label ("OA" o "UTC").
            color (str): Color para estilos QSS.
            parent (QWidget): Widget padre.
            utc (bool): Si True, muestra hora UTC; si False, hora local.
        """
        super().__init__(parent)
        self.utc = utc
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        # Label OA/UTC
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("ClockLabelOA" if not self.utc else "ClockLabelUTC")
        font_label = QFont()
        font_label.setFamily("Consolas, Menlo, Courier New, Liberation Mono, Monospace")
        font_label.setBold(True)
        font_label.setPointSize(20)
        self.label.setFont(font_label)
        # Hora
        self.time = QLabel()
        self.time.setAlignment(Qt.AlignCenter)
        self.time.setObjectName("ClockTimeOA" if not self.utc else "ClockTimeUTC")
        font_time = QFont()
        font_time.setFamily("Consolas, Menlo, Courier New, Liberation Mono, Monospace")
        font_time.setBold(True)
        font_time.setPointSize(20)
        self.time.setFont(font_time)
        # Fecha
        self.date = QLabel()
        self.date.setAlignment(Qt.AlignCenter)
        self.date.setObjectName("ClockDateOA" if not self.utc else "ClockDateUTC")
        font_date = QFont()
        font_date.setFamily("Consolas, Menlo, Courier New, Liberation Mono, Monospace")
        font_date.setPointSize(20)
        self.date.setFont(font_date)
        # Layout
        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.date)
        self.setLayout(layout)
        # Timer para actualizar cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()
        # Políticas de tamaño fijo para compactar el widget
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.time.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.date.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def update_clock(self):
        """
        Actualiza la hora y la fecha según el idioma y modo OA/UTC.
        El formato de fecha depende del idioma configurado en translation_service.
        """
        if self.utc:
            now = datetime.datetime.now(datetime.timezone.utc)
        else:
            now = datetime.datetime.now().astimezone()
        # Obtener idioma para formato de fecha
        try:
            from translation.translation_service import translation_service

            lang = translation_service.get_language()
        except Exception:
            lang = "es"
        date_fmt = "%d/%m/%Y" if lang == "es" else "%m/%d/%Y"
        self.time.setText(now.strftime("%H:%M:%S"))
        self.date.setText(now.strftime(date_fmt))
        # El texto del label es fijo: "OA" o "UTC"
        self.label.setText("OA" if not self.utc else "UTC")
