from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import datetime


class ClockWidget(QWidget):
    def __init__(self, label_text, color, parent=None, utc=False):
        super().__init__(parent)
        self.utc = utc
        layout = QHBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        if not self.utc:
            self.label.setObjectName("ClockLabelOA")
        else:
            self.label.setObjectName("ClockLabelUTC")
        font_label = QFont()
        font_label.setBold(True)
        font_label.setPointSize(20)
        self.label.setFont(font_label)
        self.time = QLabel()
        self.time.setAlignment(Qt.AlignCenter)
        if not self.utc:
            self.time.setObjectName("ClockTimeOA")
        else:
            self.time.setObjectName("ClockTimeUTC")
        font_time = QFont()
        font_time.setBold(True)
        font_time.setPointSize(20)
        self.time.setFont(font_time)
        self.date = QLabel()
        self.date.setAlignment(Qt.AlignCenter)
        if not self.utc:
            self.date.setObjectName("ClockDateOA")
        else:
            self.date.setObjectName("ClockDateUTC")
        font_date = QFont()
        font_date.setPointSize(20)
        self.date.setFont(font_date)
        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.date)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self):
        if self.utc:
            now = datetime.datetime.now(datetime.timezone.utc)
        else:
            now = datetime.datetime.now().astimezone()
        # Usar el idioma del sistema global de traducción
        try:
            from translation.translation_service import translation_service

            lang = translation_service.get_language()
        except Exception:
            lang = "es"
        date_fmt = "%d/%m/%Y" if lang == "es" else "%m/%d/%Y"
        self.time.setText(now.strftime("%H:%M:%S"))
        self.date.setText(now.strftime(date_fmt))
        # Asignar texto del label: solo "OA" o "UTC"
        self.label.setText("OA" if not self.utc else "UTC")

    def set_label_text(self, text):
        self.label.setText(text)


# Sugerencia para light.qss
# QLabel#ClockTimeOA { color: #b71c1c; }      /* Rojo oscuro */
# QLabel#ClockTimeUTC { color: #1b5e20; }     /* Verde oscuro */
# Sugerencia para dark.qss
# QLabel#ClockTimeOA { color: #ff1744; }      /* Rojo fosforescente */
# QLabel#ClockTimeUTC { color: #00e676; }     /* Verde fosforescente */
