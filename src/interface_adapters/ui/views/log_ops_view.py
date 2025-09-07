from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class LogOpsView(QWidget):
    def __init__(
        self, parent=None, callsign="", log_type_name="Operativo", log_date=""
    ):
        super().__init__(parent)
        from .log_form_widget import LogFormWidget
        from .contact_table_widget import ContactTableWidget
        from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget

        layout = QVBoxLayout()
        # Encabezado dinámico
        header_text = f"{callsign} | {log_type_name} | {log_date}"
        self.header_label = QLabel(header_text)
        self.header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header_label)
        self.form_widget = LogFormWidget(self, log_type="ops")
        layout.addWidget(self.form_widget)
        self.suggestion_widget = CallsignSuggestionWidget(self)
        layout.addWidget(self.suggestion_widget)
        self.queue_widget = ContactQueueWidget(self)
        layout.addWidget(self.queue_widget)
        self.table_widget = ContactTableWidget(self, log_type="ops")
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)

    def set_log_data(self, log):
        self._current_log = log
        self.retranslate_ui()

    def retranslate_ui(self):
        from datetime import datetime

        lang = translation_service.get_language()
        log_type_name = translation_service.tr("log_type_ops")
        log = getattr(self, "_current_log", None)
        callsign = log.operator if log else ""
        dt = log.start_time if log else ""
        try:
            date_obj = datetime.strptime(dt[:8], "%Y%m%d")
            if lang == "es":
                log_date = date_obj.strftime("%d/%m/%Y")
            else:
                log_date = date_obj.strftime("%m/%d/%Y")
        except Exception:
            log_date = dt
        header_text = f"{callsign} | {log_type_name} | {log_date}"
        self.header_label.setText(header_text)
        self.form_widget.retranslate_ui()
        self.suggestion_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
