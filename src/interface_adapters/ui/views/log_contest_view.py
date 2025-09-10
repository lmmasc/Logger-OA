from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
from .callsign_input_widget import CallsignInputWidget
from .callsign_info_widget import CallsignInfoWidget
from .clock_widget import ClockWidget


class LogContestView(QWidget):
    def __init__(self, parent=None, callsign="", log_type_name="Concurso", log_date=""):
        super().__init__(parent)
        self.callsign = callsign
        self.log_type_name = log_type_name
        self.log_date = log_date
        from .log_form_widget import LogFormWidget
        from .contact_table_widget import ContactTableWidget

        # from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)  # Márgenes reducidos
        # Encabezado dinámico eliminado
        # self.header = HeaderWidget("", self)
        # layout.addWidget(self.header)
        # Instanciar relojes y gestionar traducción
        self.oa_clock = ClockWidget(
            translation_service.tr("clock_oa_label"), "red", self, utc=False
        )
        self.utc_clock = ClockWidget(
            translation_service.tr("clock_utc_label"), "green", self, utc=True
        )
        translation_service.signal.language_changed.connect(self._retranslate_clocks)
        from PySide6.QtWidgets import QPushButton

        self.add_contact_btn = QPushButton(translation_service.tr("add_contact"), self)
        self.add_contact_btn.clicked.connect(self._on_add_contact)
        # Formulario sin botón
        self.form_widget = LogFormWidget(
            self,
            log_type="contest",
            callsign=callsign,
            log_type_name=log_type_name,
            log_date=log_date,
        )
        # Layout horizontal para relojes y botón
        clock_row = QWidget(self)
        clock_layout = QHBoxLayout(clock_row)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_layout.setSpacing(16)
        clock_layout.addWidget(self.oa_clock)
        clock_layout.addWidget(self.utc_clock)
        clock_layout.addWidget(self.add_contact_btn)
        clock_row.setLayout(clock_layout)
        layout.addWidget(clock_row)
        layout.addWidget(self.form_widget)
        # Nuevo bloque: input y área de info
        self.callsign_input = CallsignInputWidget(self)
        self.callsign_info = CallsignInfoWidget(self)
        layout.addWidget(self.callsign_input)
        layout.addWidget(self.callsign_info)
        # Conexión de sugerencias
        self.callsign_info.suggestionSelected.connect(self.callsign_input.set_callsign)
        # Actualización dinámica del área de info
        self.callsign_input.input.textChanged.connect(self.callsign_info.update_info)
        self.callsign_info.update_info(self.callsign_input.get_callsign())
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)

        # Header
        from .header_widget import HeaderWidget

        self.header_widget = HeaderWidget()
        layout.addWidget(self.header_widget)

        self.table_widget = ContactTableWidget(self, log_type="contest")
        layout.addWidget(self.table_widget)
        from .contact_queue_widget import ContactQueueWidget

        self.queue_widget = ContactQueueWidget(self)
        layout.addWidget(self.queue_widget)

        self.update_header()
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
        self.header_widget.update_text(header_text)
        self.form_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()

    def update_header(self):
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
        from datetime import datetime

        lang = translation_service.get_language()
        try:
            date_obj = datetime.strptime(dt[:8], "%Y%m%d")
            if lang == "es":
                log_date = date_obj.strftime("%d/%m/%Y")
            else:
                log_date = date_obj.strftime("%m/%d/%Y")
        except Exception:
            log_date = dt
        header_text = f"{self.log_type_name} - {callsign} - {log_date}"
        self.header_widget.update_text(header_text)

    def _update_callsign_info(self):
        filtro = self.callsign_input.get_callsign().strip()
        if filtro:
            if len(filtro) < 3:
                self.callsign_info.show_suggestions(filtro)
            else:
                from infrastructure.repositories.sqlite_radio_operator_repository import (
                    SqliteRadioOperatorRepository,
                )

                repo = SqliteRadioOperatorRepository()
                operator = repo.get_operator_by_callsign(filtro)
                if operator:
                    resumen = f"{operator.callsign} - {operator.name}"
                    self.callsign_info.show_summary(resumen)
                else:
                    self.callsign_info.show_summary(
                        translation_service.tr("callsign_not_found")
                    )
        else:
            self.callsign_info.show_suggestions("")

    def _retranslate_clocks(self):
        self.oa_clock.set_label_text(translation_service.tr("clock_oa_label"))
        self.utc_clock.set_label_text(translation_service.tr("clock_utc_label"))

    def _on_add_contact(self):
        callsign = self.callsign_input.get_callsign().strip()
        self.form_widget._on_add_contact(callsign)
        # Limpiar campo y poner foco
        self.callsign_input.input.clear()
        self.callsign_input.input.setFocus()
        # Eliminar de la cola si está presente
        items = [
            self.queue_widget.queue_list.item(i).text()
            for i in range(self.queue_widget.queue_list.count())
        ]
        if callsign in items:
            for i in range(self.queue_widget.queue_list.count()):
                if self.queue_widget.queue_list.item(i).text() == callsign:
                    self.queue_widget.queue_list.takeItem(i)
                    break
