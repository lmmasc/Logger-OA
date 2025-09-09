from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class LogOpsView(QWidget):
    def __init__(
        self, parent=None, callsign="", log_type_name="Operativo", log_date=""
    ):
        super().__init__(parent)
        self.callsign = callsign
        self.log_type_name = log_type_name
        self.log_date = log_date
        from .log_form_widget import LogFormWidget
        from .contact_table_widget import ContactTableWidget
        from .header_widget import HeaderWidget

        # from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget
        from .callsign_input_widget import CallsignInputWidget
        from .callsign_info_widget import CallsignInfoWidget

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        # Encabezado dinámico eliminado
        self.header_widget = HeaderWidget()
        layout.addWidget(self.header_widget)
        self.form_widget = LogFormWidget(
            self,
            log_type="ops",
            callsign=callsign,
            log_type_name=log_type_name,
            log_date=log_date,
        )
        self.queue_widget = ContactQueueWidget(self)
        layout.addWidget(self.queue_widget)
        # El formulario ya no tiene altura fija, solo política preferida
        from PySide6.QtWidgets import QSizePolicy

        self.form_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.form_widget)
        self.table_widget = ContactTableWidget(self, log_type="ops")
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.table_widget)
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

        # self.form_widget.callsign_input.addToQueue.connect(
        #     self.queue_widget.add_to_queue
        # )
        # self.queue_widget.setCallsign.connect(
        #     self.form_widget.callsign_input.input.setText
        # )
        self.update_header()

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
        meta = getattr(log, "metadata", {}) if log else {}
        tipo = translation_service.tr(meta.get("tipo_key", "")) if meta else ""
        banda = translation_service.tr(meta.get("banda_key", "")) if meta else ""
        modo = translation_service.tr(meta.get("modo_key", "")) if meta else ""
        freq = meta.get("frecuencia", "") if meta else ""
        rep = (
            translation_service.tr(meta.get("repetidora_key", ""))
            if meta and meta.get("repetidora_key")
            else ""
        )
        try:
            date_obj = datetime.strptime(dt[:8], "%Y%m%d")
            if lang == "es":
                log_date = date_obj.strftime("%d/%m/%Y")
            else:
                log_date = date_obj.strftime("%m/%d/%Y")
        except Exception:
            log_date = dt
        header_parts = [callsign, tipo, banda, modo, freq]
        if rep:
            header_parts.append(rep)
        header_parts.append(log_date)
        header_text = " | ".join([str(p) for p in header_parts if p])
        self.header_widget.update_text(header_text)
        self.form_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()

    def update_header(self):
        header_text = f"{self.log_type_name} - {self.callsign} - {self.log_date}"
        self.header_widget.update_text(header_text)

    def _update_callsign_info(self):
        filtro = self.callsign_input.get_callsign().strip()
        if filtro:
            # Si hay texto, mostrar sugerencias si el texto es corto, si no mostrar resumen
            if len(filtro) < 3:
                self.callsign_info.show_suggestions(filtro)
            else:
                # Buscar operador y mostrar resumen si existe
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
