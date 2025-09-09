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

        # from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)  # Márgenes reducidos
        # Encabezado dinámico
        header_text = f"{callsign} | {log_type_name} | {log_date}"
        self.header_label = QLabel(header_text)
        self.header_label.setAlignment(Qt.AlignCenter)
        header_font = self.header_label.font()
        header_font.setPointSize(18)  # Fuente ajustada
        header_font.setBold(True)
        self.header_label.setFont(header_font)
        layout.addWidget(self.header_label)
        self.form_widget = LogFormWidget(self, log_type="ops")
        self.queue_widget = ContactQueueWidget(self)
        # layout.addWidget(self.form_widget)
        # layout.addWidget(self.queue_widget)
        # Nuevo orden: primero el widget de ingreso de indicativo, luego la cola, luego el formulario
        layout.addWidget(self.form_widget.callsign_input)
        layout.addWidget(self.queue_widget)
        # Agregar el resto del formulario
        layout.addWidget(self.form_widget)
        # CallsignSuggestionWidget eliminado
        self.table_widget = ContactTableWidget(self, log_type="ops")
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)

        self.form_widget.callsign_input.addToQueue.connect(
            self.queue_widget.add_to_queue
        )
        self.queue_widget.setCallsign.connect(
            self.form_widget.callsign_input.input.setText
        )

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
        # Cabecera extendida
        header_parts = [callsign, tipo, banda, modo, freq]
        if rep:
            header_parts.append(rep)
        header_parts.append(log_date)
        header_text = " | ".join([str(p) for p in header_parts if p])
        self.header_label.setText(header_text)
        self.form_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
