from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class LogContestView(QWidget):
    def __init__(self, parent=None, callsign="", log_type_name="Concurso", log_date=""):
        super().__init__(parent)
        from .log_form_widget import LogFormWidget
        from .contact_table_widget import ContactTableWidget

        # from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)  # Márgenes reducidos
        # Encabezado dinámico eliminado
        # self.header = HeaderWidget("", self)
        # layout.addWidget(self.header)
        self.form_widget = LogFormWidget(
            self,
            log_type="contest",
            callsign=callsign,
            log_type_name=log_type_name,
            log_date=log_date,
        )
        layout.addWidget(self.form_widget)
        # CallsignSuggestionWidget eliminado
        self.queue_widget = ContactQueueWidget(self)
        layout.addWidget(self.queue_widget)
        self.table_widget = ContactTableWidget(self, log_type="contest")
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def set_log_data(self, log):
        # Actualiza los datos del log y refresca la cabecera
        self._current_log = log
        self.retranslate_ui()

    def retranslate_ui(self):
        from datetime import datetime

        lang = translation_service.get_language()
        log = getattr(self, "_current_log", None)
        callsign = log.operator if log else ""
        contest_key = (
            log.metadata.get("contest_name_key", None)
            if log and hasattr(log, "metadata")
            else None
        )
        contest_name = (
            translation_service.tr(contest_key)
            if contest_key
            else translation_service.tr("log_type_contest")
        )
        dt = log.start_time if log else ""
        try:
            date_obj = datetime.strptime(dt[:8], "%Y%m%d")
            if lang == "es":
                log_date = date_obj.strftime("%d/%m/%Y")
            else:
                log_date = date_obj.strftime("%m/%d/%Y")
        except Exception:
            log_date = dt
        header_text = f"{callsign} | {contest_name} | {log_date}"
        self.form_widget.update_header(header_text)
        self.form_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
