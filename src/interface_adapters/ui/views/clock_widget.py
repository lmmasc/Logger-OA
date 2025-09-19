"""
ClockWidget

Widget de reloj digital con soporte OA/UTC y formato de fecha/hora dependiente de idioma.
- Compatible multiplataforma (fuente monoespaciada).
- Actualiza cada segundo.
- Colores y estilos configurables vía QSS.
- Soporte para formato de fecha según idioma y modo OA/UTC.
"""

# --- Imports estándar ---
import datetime

# --- Imports de terceros ---
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from utils.resources import get_resource_path
from PySide6.QtGui import QFontDatabase

# --- Imports de la aplicación ---
from translation.translation_service import translation_service
from config.settings_service import LanguageValue


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
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("ClockLabelOA" if not self.utc else "ClockLabelUTC")
        font_label = QFont()
        font_label.setFamily("Consolas, Menlo, Courier New, Liberation Mono, Monospace")
        font_label.setBold(True)
        font_label.setPointSize(20)
        self.label.setFont(font_label)
        # Hora
        self.time = QLabel()
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time.setObjectName("ClockTimeOA" if not self.utc else "ClockTimeUTC")
        font_path = get_resource_path("assets/RobotoMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font_time = QFont()
        if font_families:
            font_time.setFamily(font_families[0])
        else:
            font_time.setFamily(
                "Consolas, Menlo, Courier New, Liberation Mono, Monospace"
            )
        font_time.setBold(True)
        font_time.setPointSize(20)
        self.time.setFont(font_time)
        # Fecha
        self.date = QLabel()
        self.date.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date.setObjectName("ClockDateOA" if not self.utc else "ClockDateUTC")
        font_date = QFont()
        if font_families:
            font_date.setFamily(font_families[0])
        else:
            font_date.setFamily(
                "Consolas, Menlo, Courier New, Liberation Mono, Monospace"
            )
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
        self.label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.time.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.date.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

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
            lang = translation_service.get_language()
        except Exception:
            lang = LanguageValue.ES
        if lang == LanguageValue.ES:
            date_fmt = "%d/%m/%Y"
        else:
            date_fmt = "%m/%d/%Y"
        self.time.setText(now.strftime("%H:%M:%S"))
        self.date.setText(now.strftime(date_fmt))
        # El texto del label es fijo: "OA" o "UTC"
        self.label.setText("OA" if not self.utc else "UTC")
