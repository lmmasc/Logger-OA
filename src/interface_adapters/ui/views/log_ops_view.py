"""
Vista principal para la gestión de logs operativos (LogOpsView).
Incluye formulario, cola de contactos, tabla y área de información de indicativos.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
from .log_form_widget import LogFormWidget
from .contact_table_widget import ContactTableWidget
from .header_widget import HeaderWidget
from .contact_queue_widget import ContactQueueWidget
from .callsign_input_widget import CallsignInputWidget
from .callsign_info_widget import CallsignInfoWidget
from .clock_widget import ClockWidget


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
        # Formulario sin botón
        self.form_widget = LogFormWidget(
            self,
            log_type="ops",
            callsign=callsign,
            log_type_name=log_type_name,
            log_date=log_date,
        )
        self.form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.form_widget)

        # Instanciar relojes sin traducción de label
        self.oa_clock = ClockWidget("OA", "red", self, utc=False)
        self.utc_clock = ClockWidget("UTC", "green", self, utc=True)
        from PySide6.QtWidgets import QPushButton

        self.add_contact_btn = QPushButton(translation_service.tr("add_contact"), self)
        self.add_contact_btn.setObjectName("AddContactButton")
        self.add_contact_btn.clicked.connect(self._on_add_contact)
        self.delete_contact_btn = QPushButton(
            translation_service.tr("delete_contact"), self
        )
        self.delete_contact_btn.setObjectName("DeleteContactButton")
        self.delete_contact_btn.setEnabled(False)
        self.delete_contact_btn.clicked.connect(self._on_delete_contact)
        # Layout horizontal para relojes y botón
        clock_row = QWidget(self)
        clock_layout = QHBoxLayout(clock_row)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_layout.setSpacing(16)
        clock_layout.addWidget(self.oa_clock)
        clock_layout.addWidget(self.utc_clock)
        clock_layout.addWidget(self.add_contact_btn)
        clock_layout.addWidget(self.delete_contact_btn)
        clock_row.setLayout(clock_layout)
        layout.addWidget(clock_row)
        self.table_widget = ContactTableWidget(
            self, log_type="ops"
        )  # Persistencia diferenciada por log_type
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.table_widget)
        # Habilitar el botón de eliminar solo si hay una fila seleccionada
        self.table_widget.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.queue_widget.setCallsign.connect(self.callsign_input.set_callsign)
        self.callsign_input.addToQueue.connect(self.queue_widget.add_to_queue)
        self.callsign_info.suggestionSelected.connect(self.callsign_input.set_callsign)
        self.callsign_input.input.textChanged.connect(self.callsign_info.update_info)
        self.callsign_info.update_info(self.callsign_input.get_callsign())
        self.setLayout(layout)
        # Conexión de señales para refresco de UI y relojes al cambiar idioma
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        translation_service.signal.language_changed.connect(self._retranslate_clocks)
        self.update_header()

    def _retranslate_clocks(self):
        """
        Refresca el formato de fecha/hora de los relojes OA y UTC al cambiar idioma.
        """
        self.oa_clock.update_clock()
        self.utc_clock.update_clock()
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
        operation_type = (
            translation_service.tr(meta.get("operation_type", "")) if meta else ""
        )
        frequency_band = (
            translation_service.tr(meta.get("frequency_band", "")) if meta else ""
        )
        mode = translation_service.tr(meta.get("mode_key", "")) if meta else ""
        freq = meta.get("frequency", "") if meta else ""
        repeater = (
            translation_service.tr(meta.get("repeater_key", ""))
            if meta and meta.get("repeater_key")
            else ""
        )
        log_date = meta.get("log_date", "") if meta else ""
        header_parts = [callsign, operation_type, frequency_band, mode, freq]
        header_parts.append(log_date)
        header_text = " | ".join([str(p) for p in header_parts if p])
        self.header_widget.update_text(header_text)
        self.form_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
        # Actualizar textos de los botones de agregar y eliminar
        if hasattr(self, "add_contact_btn"):
            self.add_contact_btn.setText(translation_service.tr("add_contact"))
        if hasattr(self, "delete_contact_btn"):
            self.delete_contact_btn.setText(translation_service.tr("delete_contact"))

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
                    from PySide6.QtWidgets import QMessageBox

                    msg_box = QMessageBox(self)
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setWindowTitle(
                        translation_service.tr("invalid_callsign_title")
                    )
                    msg_box.setText(translation_service.tr("invalid_callsign_msg"))
                    msg_box.setInformativeText(
                        f"{translation_service.tr('callsign_not_found')}: {filtro}"
                    )
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec()
                    self.callsign_info.show_summary(
                        translation_service.tr("callsign_not_found")
                    )
        else:
            self.callsign_info.show_suggestions("")

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

    def _find_main_window(self):
        """
        Busca la instancia de MainWindow en la jerarquía de padres.
        Returns:
            MainWindow instance o None
        """
        parent = self.parent()
        while parent:
            if parent.__class__.__name__ == "MainWindow":
                return parent
            parent = parent.parent()
        return None

    def _on_delete_contact(self):
        # Eliminar contacto seleccionado de la tabla solo si hay una fila seleccionada
        selected_items = self.table_widget.table.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        contact_list = (
            self.table_widget._last_contacts
            if hasattr(self.table_widget, "_last_contacts")
            else []
        )
        if row >= len(contact_list):
            return
        contact = contact_list[row]
        contact_id = contact.get("id", None)
        callsign = contact.get("callsign", "")
        name = contact.get("name", "")
        # Mostrar diálogo de confirmación
        from PySide6.QtWidgets import QMessageBox

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(translation_service.tr("delete_contact"))
        msg_box.setText(translation_service.tr("confirm_delete_contact"))
        msg_box.setInformativeText(
            f"{translation_service.tr('table_header_callsign')}: {callsign}\n{translation_service.tr('table_header_name')}: {name}"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        yes_button = msg_box.button(QMessageBox.Yes)
        no_button = msg_box.button(QMessageBox.No)
        yes_button.setText(translation_service.tr("yes_button"))
        no_button.setText(translation_service.tr("no_button"))
        reply = msg_box.exec()
        if reply != QMessageBox.Yes:
            return
        # Eliminar usando el caso de uso
        main_window = self._find_main_window()
        if (
            not main_window
            or not hasattr(main_window, "current_log")
            or not main_window.current_log
        ):
            return
        db_path = getattr(main_window.current_log, "db_path", None)
        log_id = getattr(main_window.current_log, "id", None)
        from application.use_cases.contact_management import delete_contact_from_log

        delete_contact_from_log(db_path, contact_id)
        # Actualizar la tabla
        from domain.repositories.contact_log_repository import ContactLogRepository

        repo = ContactLogRepository(db_path)
        contacts = repo.get_contacts(log_id)
        main_window.current_log.contacts = contacts
        self.table_widget.set_contacts(contacts)

    def _on_selection_changed(self):
        selected_rows = self.table_widget.table.selectionModel().selectedRows()
        self.delete_contact_btn.setEnabled(len(selected_rows) == 1)
