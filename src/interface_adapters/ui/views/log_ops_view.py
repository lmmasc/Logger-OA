"""
Vista principal para la gestión de logs operativos (LogOpsView).
Incluye formulario, cola de contactos, tabla y área de información de indicativos.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt
from translation.translation_service import translation_service

from .log_form_widget import LogFormWidget
from .contact_table_widget import ContactTableWidget
from .header_widget import HeaderWidget
from .contact_queue_widget import ContactQueueWidget
from .callsign_input_widget import CallsignInputWidget
from .callsign_info_widget import CallsignInfoWidget
from .clock_widget import ClockWidget
from interface_adapters.ui.view_manager import LogType
from application.use_cases.contact_management import (
    delete_contact_from_log,
    ContactLogRepository,
)
from interface_adapters.ui.utils import find_main_window
from infrastructure.repositories.sqlite_radio_operator_repository import (
    SqliteRadioOperatorRepository,
)
from datetime import datetime


class LogOpsView(QWidget):
    """
    Vista principal para la gestión de logs operativos.
    Permite visualizar y editar contactos, gestionar la cola y mostrar información de indicativos.
    """

    def __init__(self, parent=None, callsign="", log_date=""):
        """
        Inicializa la vista de log operativo, configurando todos los componentes visuales y sus conexiones.
        Args:
            parent: QWidget padre.
            callsign: Indicativo inicial.
            log_date: Fecha del log.
        """
        super().__init__(parent)
        self.callsign = callsign
        self.log_date = log_date
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.header_widget = HeaderWidget()
        self.header_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.header_widget)
        # Widgets de indicativo en una misma fila
        indicativo_row = QWidget(self)
        indicativo_layout = QHBoxLayout(indicativo_row)
        indicativo_layout.setContentsMargins(10, 0, 10, 0)
        indicativo_layout.setSpacing(8)
        indicativo_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.callsign_input = CallsignInputWidget(indicativo_row)
        self.callsign_input.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.callsign_info = CallsignInfoWidget(indicativo_row)
        self.callsign_info.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        indicativo_layout.addWidget(self.callsign_input)
        indicativo_layout.addWidget(self.callsign_info)
        indicativo_row.setLayout(indicativo_layout)
        indicativo_row.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(indicativo_row)
        self.queue_widget = ContactQueueWidget(self)
        self.queue_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.queue_widget)
        # Formulario sin botón
        self.form_widget = LogFormWidget(self, log_type=LogType.OPERATION_LOG)
        self.form_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        layout.addWidget(self.form_widget)

        # Instanciar relojes sin traducción de label
        self.oa_clock = ClockWidget("OA", "red", self, utc=False)
        self.utc_clock = ClockWidget("UTC", "green", self, utc=True)

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
        clock_layout.setContentsMargins(10, 0, 10, 0)
        clock_layout.setSpacing(8)
        clock_layout.addWidget(self.oa_clock)
        clock_layout.addWidget(self.utc_clock)
        clock_layout.addWidget(self.add_contact_btn)
        clock_layout.addWidget(self.delete_contact_btn)
        clock_row.setLayout(clock_layout)
        layout.addWidget(clock_row)
        self.table_widget = ContactTableWidget(
            self, log_type=LogType.OPERATION_LOG
        )  # Persistencia diferenciada por log_type
        self.table_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.table_widget)
        # Habilitar el botón de eliminar solo si hay una fila seleccionada
        self.table_widget.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.queue_widget.setCallsign.connect(self.callsign_input.set_callsign)
        self.callsign_input.addToQueue.connect(self.queue_widget.add_to_queue)
        self.callsign_info.suggestionSelected.connect(self._on_suggestion_selected)
        self.callsign_input.input.textChanged.connect(self.callsign_info.update_info)
        self.callsign_info.update_info(self.callsign_input.get_callsign())
        self.setLayout(layout)
        # Conexión de señales para refresco de UI y relojes al cambiar idioma
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self.update_header()
        # Evitar foco en cola y tabla
        self.queue_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.callsign_info.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.callsign_input.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.header_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.form_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if hasattr(self.queue_widget, "queue_list"):
            self.queue_widget.queue_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if hasattr(self.table_widget, "table"):
            self.table_widget.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.add_contact_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.delete_contact_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Orden de tabulación: input de indicativo -> primer campo del formulario
        if hasattr(self.form_widget, "station_input"):
            QWidget.setTabOrder(
                self.callsign_input.input, self.form_widget.station_input
            )
            QWidget.setTabOrder(
                self.form_widget.station_input, self.form_widget.energy_input
            )
            QWidget.setTabOrder(
                self.form_widget.energy_input, self.form_widget.power_input
            )
            QWidget.setTabOrder(
                self.form_widget.power_input, self.form_widget.rs_rx_input
            )
            QWidget.setTabOrder(
                self.form_widget.rs_rx_input, self.form_widget.rs_tx_input
            )
            QWidget.setTabOrder(
                self.form_widget.rs_tx_input, self.form_widget.observations_input
            )

    def set_log_data(self, log):
        """
        Asigna los datos del log actual y refresca la UI.
        Args:
            log: Objeto log con los datos a mostrar.
        """
        self._current_log = log
        self.retranslate_ui()

    def retranslate_ui(self):
        """
        Actualiza los textos de la UI según el idioma seleccionado y los datos del log, y refresca relojes.
        """
        # Actualizar relojes OA y UTC
        self.oa_clock.update_clock()
        self.utc_clock.update_clock()

        # Actualizar encabezado usando la lógica centralizada
        self.update_header()

        self.form_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
        # Actualizar textos de los botones de agregar y eliminar
        if hasattr(self, "add_contact_btn"):
            self.add_contact_btn.setText(translation_service.tr("add_contact"))
        if hasattr(self, "delete_contact_btn"):
            self.delete_contact_btn.setText(translation_service.tr("delete_contact"))

    def update_header(self):
        """
        Actualiza el texto del encabezado principal de la vista usando la misma lógica que retranslate_ui.
        """
        log = getattr(self, "_current_log", None)
        callsign = log.operator if log else ""
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
        show_freq = True
        if frequency_band.lower() == translation_service.tr("vhf").lower():
            repeater_key = meta.get("repeater_key", "")
            if repeater_key and repeater_key != "rep_simplex":
                show_freq = False
        header_parts = [callsign, operation_type, frequency_band, mode]
        if show_freq and freq:
            header_parts.append(freq)
        if repeater:
            header_parts.append(repeater)
        header_parts.append(log_date)
        header_text = " | ".join([str(p) for p in header_parts if p])
        self.header_widget.update_text(header_text)

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
                repo = SqliteRadioOperatorRepository()
                operator = repo.get_operator_by_callsign(filtro)
                if operator:
                    resumen = f"{operator.callsign} - {operator.name}"
                    self.callsign_info.show_summary(resumen)
                else:
                    msg_box = QMessageBox(self)
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setWindowTitle(
                        translation_service.tr("dialog_invalid_callsign_title")
                    )
                    msg_box.setText(
                        translation_service.tr("dialog_invalid_callsign_msg")
                    )
                    msg_box.setInformativeText(
                        f"{translation_service.tr('callsign_not_found')}: {filtro}"
                    )
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg_box.exec()
                    self.callsign_info.show_summary(
                        translation_service.tr("callsign_not_found")
                    )
        else:
            self.callsign_info.show_suggestions("")

    def _on_suggestion_selected(self, callsign):
        """
        Maneja la selección de una sugerencia de indicativo.
        Actualiza el campo de entrada y la información mostrada, y da foco al primer campo del formulario.
        Args:
            callsign: Indicativo seleccionado.
        """
        self.callsign_input.set_callsign(callsign)
        self.callsign_info.update_info(callsign)
        # Foco al primer campo del formulario
        if hasattr(self.form_widget, "station_input"):
            self.form_widget.station_input.setFocus()

    def _on_add_contact(self):
        """
        Agrega un nuevo contacto al log y actualiza la UI y la cola de contactos.
        """
        callsign = self.callsign_input.get_callsign().strip()
        result = self.form_widget._on_add_contact(callsign)
        if result:  # Solo si el contacto se agregó correctamente
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

    def _on_delete_contact(self):
        """
        Elimina el contacto seleccionado de la tabla, tras confirmación del usuario y actualización en la base de datos.
        """
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
        # Sincronizar el índice visual con el real (por inversión en la tabla)
        real_index = len(contact_list) - 1 - row
        if real_index < 0 or real_index >= len(contact_list):
            return
        contact = contact_list[real_index]
        contact_id = contact.get("id", None)
        callsign = contact.get("callsign", "")
        name = contact.get("name", "")
        # Mostrar diálogo de confirmación
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle(translation_service.tr("delete_contact"))
        msg_box.setText(translation_service.tr("dialog_confirm_delete_contact"))
        msg_box.setInformativeText(
            f"{translation_service.tr('log_operative_table_header_callsign')}: {callsign}\n{translation_service.tr('log_operative_table_header_name')}: {name}"
        )
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
        no_button = msg_box.button(QMessageBox.StandardButton.No)
        reply = msg_box.exec()
        if reply != QMessageBox.StandardButton.Yes:
            return
        # Validar existencia de current_log y sus atributos
        main_window = find_main_window(self)
        if not main_window or not hasattr(main_window, "current_log"):
            return
        current_log = main_window.current_log
        if not current_log or not hasattr(current_log, "db_path"):
            return
        db_path = current_log.db_path
        log_id = getattr(current_log, "id", None)
        if db_path is None or log_id is None or contact_id is None:
            return

        delete_contact_from_log(db_path, contact_id)
        repo = ContactLogRepository(db_path)
        contacts = repo.get_contacts(log_id)
        # Validar que current_log tiene atributo contacts
        if hasattr(current_log, "contacts"):
            current_log.contacts = contacts
        self.table_widget.set_contacts(contacts)

    def _on_selection_changed(self):
        """
        Habilita o deshabilita el botón de eliminar según si hay una fila seleccionada en la tabla de contactos.
        """
        selected_rows = self.table_widget.table.selectionModel().selectedRows()
        self.delete_contact_btn.setEnabled(len(selected_rows) == 1)
