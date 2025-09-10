"""
Vista principal para la gestión de logs operativos (LogOpsView).
Incluye formulario, cola de contactos, tabla y área de información de indicativos.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
from .log_form_widget import LogFormWidget
from .contact_table_widget import ContactTableWidget
from .header_widget import HeaderWidget
from .contact_queue_widget import ContactQueueWidget
from .callsign_input_widget import CallsignInputWidget
from .callsign_info_widget import CallsignInfoWidget


class LogOpsView(QWidget):
    """
    Vista principal para la gestión de logs operativos.
    Permite visualizar y editar contactos, gestionar la cola y mostrar información de indicativos.
    """

    def __init__(
        self, parent=None, callsign="", log_type_name="Operativo", log_date=""
    ):
        """
        Inicializa la vista de log operativo, configurando todos los componentes visuales y sus conexiones.
        Args:
            parent: QWidget padre.
            callsign: Indicativo inicial.
            log_type_name: Nombre del tipo de log.
            log_date: Fecha del log.
        """
        super().__init__(parent)
        self.callsign = callsign
        self.log_type_name = log_type_name
        self.log_date = log_date
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        self.header_widget = HeaderWidget()
        self.header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.header_widget)
        # Widgets de indicativo en una misma fila
        from PySide6.QtWidgets import QHBoxLayout, QWidget

        indicativo_row = QWidget(self)
        indicativo_layout = QHBoxLayout(indicativo_row)
        indicativo_layout.setContentsMargins(0, 0, 0, 0)
        indicativo_layout.setSpacing(8)
        indicativo_layout.setAlignment(Qt.AlignVCenter)
        self.callsign_input = CallsignInputWidget(indicativo_row)
        self.callsign_input.setFixedWidth(320)
        self.callsign_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.callsign_info = CallsignInfoWidget(indicativo_row)
        self.callsign_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        indicativo_layout.addWidget(self.callsign_input)
        indicativo_layout.addWidget(self.callsign_info)
        indicativo_row.setLayout(indicativo_layout)
        indicativo_row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(indicativo_row)
        self.queue_widget = ContactQueueWidget(self)
        self.queue_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.queue_widget)
        self.form_widget = LogFormWidget(
            self,
            log_type="ops",
            callsign=callsign,
            log_type_name=log_type_name,
            log_date=log_date,
        )
        self.form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.form_widget)
        self.table_widget = ContactTableWidget(self, log_type="ops")
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.table_widget)
        self.callsign_info.suggestionSelected.connect(self.callsign_input.set_callsign)
        self.callsign_input.input.textChanged.connect(self.callsign_info.update_info)
        self.callsign_info.update_info(self.callsign_input.get_callsign())
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self.update_header()

    def update_header(self):
        """
        Actualiza el texto del encabezado principal de la vista.
        """
        header_text = f"{self.log_type_name} - {self.callsign} - {self.log_date}"
        self.header_widget.update_text(header_text)

    def set_log_data(self, log):
        """
        Asigna un log actual y actualiza la UI con los datos correspondientes.
        Args:
            log: Objeto de log operativo.
        """
        self._current_log = log
        self.retranslate_ui()

    def retranslate_ui(self):
        """
        Actualiza los textos de la UI según el idioma seleccionado y los datos del log.
        """
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

    def _update_callsign_info(self):
        """
        Actualiza el área de información de indicativos según el texto ingresado.
        Muestra sugerencias si el texto es corto, o el resumen si hay coincidencia exacta.
        """
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
