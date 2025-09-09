from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QLocale
import datetime


class ClockWidget(QWidget):
    def __init__(self, label_text, color, parent=None, utc=False):
        super().__init__(parent)
        self.utc = utc
        layout = QHBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.time = QLabel()
        self.time.setAlignment(Qt.AlignCenter)
        self.time.setStyleSheet(f"color: {color}; font-size: 30px; font-weight: bold;")
        self.date = QLabel()
        self.date.setAlignment(Qt.AlignCenter)
        self.date.setStyleSheet(f"color: {color};")
        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.date)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.utcnow() if self.utc else datetime.datetime.now()
        lang = QLocale().name()
        date_fmt = "%d/%m/%Y" if lang.startswith("es") else "%m/%d/%Y"
        self.time.setText(now.strftime("%H:%M:%S"))
        self.date.setText(now.strftime(date_fmt))

    def set_label_text(self, text):
        self.label.setText(text)
