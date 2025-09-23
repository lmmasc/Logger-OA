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
from utils.callsign_parser import parse_callsign


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
        # Eliminado HeaderWidget
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
        # Botón QRZ
        self.qrz_btn = QPushButton("QRZ", self)
        self.qrz_btn.setObjectName("QRZButton")
        self.qrz_btn.setToolTip("Abrir QRZ.com para el indicativo")
        self.qrz_btn.clicked.connect(self._on_open_qrz)
        # Layout horizontal para relojes y botón
        clock_row = QWidget(self)
        clock_layout = QHBoxLayout(clock_row)
        clock_layout.setContentsMargins(10, 0, 10, 0)
        clock_layout.setSpacing(8)
        clock_layout.addWidget(self.oa_clock)
        clock_layout.addWidget(self.utc_clock)
        clock_layout.addWidget(self.add_contact_btn)
        clock_layout.addWidget(self.delete_contact_btn)
        clock_layout.addWidget(self.qrz_btn)
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
        self.callsign_input.addContactRequested.connect(self._on_add_contact)
        self.callsign_info.suggestionSelected.connect(self._on_suggestion_selected)
        self.callsign_input.input.textChanged.connect(self.callsign_info.update_info)
        self.callsign_info.update_info(self.callsign_input.get_callsign())
        self.setLayout(layout)
        # Conexión de señales para refresco de UI y relojes al cambiar idioma
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self.update_header()
        # Evitar foco en cola y tabla
        self.queue_widget.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.callsign_info.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.callsign_input.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.form_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if hasattr(self.queue_widget, "queue_list"):
            self.queue_widget.queue_list.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        if hasattr(self.table_widget, "table"):
            self.table_widget.table.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.add_contact_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.delete_contact_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.qrz_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        # Instalar eventFilter para F1 en toda la vista
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        from PySide6.QtCore import QEvent, Qt

        # Detectar teclas F1-F4 en toda la ventana
        if event.type() == QEvent.KeyPress:  # type: ignore
            # F1: foco al campo input de indicativo
            if event.key() == Qt.Key_F1:  # type: ignore
                if hasattr(self, "callsign_input") and hasattr(
                    self.callsign_input, "input"
                ):
                    self.callsign_input.input.setFocus()
                    return True
            # F2: foco a sugerencias
            if event.key() == Qt.Key_F2:  # type: ignore
                if hasattr(self, "callsign_info") and hasattr(
                    self.callsign_info, "suggestion_list"
                ):
                    self.callsign_info.suggestion_list.setFocus()
                    return True
            # F3: foco a cola de espera
            if event.key() == Qt.Key_F3:  # type: ignore
                if hasattr(self, "queue_widget"):
                    # Si tiene queue_list, enfocar ese; si no, el widget principal
                    if hasattr(self.queue_widget, "queue_list"):
                        self.queue_widget.queue_list.setFocus()
                    else:
                        self.queue_widget.setFocus()
                    return True
            # F4: foco a la tabla de contactos
            if event.key() == Qt.Key_F4:  # type: ignore
                if hasattr(self, "table_widget") and hasattr(
                    self.table_widget, "table"
                ):
                    self.table_widget.table.setFocus()
                    return True
            # Suprimir: eliminar contacto si el botón está habilitado
            if event.key() == Qt.Key_Delete:  # type: ignore
                if (
                    hasattr(self, "delete_contact_btn")
                    and self.delete_contact_btn.isEnabled()
                ):
                    self.delete_contact_btn.click()
                    return True
        return super().eventFilter(obj, event)

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

        self.callsign_info.update_info(self.callsign_input.get_callsign())

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
        # Obtener start_time y formatear a string dd/mm/yyyy con hora de Perú
        log_date = ""
        if log and hasattr(log, "start_time") and log.start_time:
            from datetime import datetime, timezone, timedelta

            dt_utc = datetime.fromtimestamp(log.start_time, tz=timezone.utc)
            dt_peru = dt_utc - timedelta(hours=5)
            log_date = dt_peru.strftime("%d/%m/%Y %H:%M")
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
        header_text = " - ".join([str(p) for p in header_parts if p])
        # Solo actualizar el título de la ventana principal si la vista está visible
        from interface_adapters.ui.utils import find_main_window

        main_window = find_main_window(self)
        if self.isVisible() and main_window and hasattr(main_window, "setWindowTitle"):
            main_window.setWindowTitle(header_text)

    def _on_suggestion_selected(self, base_callsign):
        """
        Maneja la selección de una sugerencia de indicativo.
        Actualiza el campo de entrada y la información mostrada, manteniendo prefijo/sufijo originales, y da foco al primer campo del formulario.
        Args:
            base_callsign: Indicativo base seleccionado.
        """
        # Obtener el indicativo actual
        current = self.callsign_input.get_callsign()

        base, prefijo, sufijo = parse_callsign(current)
        # Reconstruir manteniendo prefijo/sufijo
        nuevo = base_callsign
        if prefijo and not base_callsign.startswith(f"{prefijo}/"):
            nuevo = f"{prefijo}/{nuevo}"
        if sufijo and not base_callsign.endswith(f"/{sufijo}"):
            nuevo = f"{nuevo}/{sufijo}"
        self.callsign_input.set_callsign(nuevo)
        self.callsign_info.update_info(nuevo)
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

    def _on_open_qrz(self):
        callsign = self.callsign_input.get_callsign().strip()
        if not callsign:
            QMessageBox.warning(
                self, "QRZ", translation_service.tr("dialog_no_callsign_entered")
            )
            return
        import webbrowser

        url = f"https://www.qrz.com/db/{callsign}"
        webbrowser.open(url)
