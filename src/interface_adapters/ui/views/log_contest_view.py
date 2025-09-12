from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from translation.translation_service import translation_service
from .callsign_input_widget import CallsignInputWidget
from .callsign_info_widget import CallsignInfoWidget
from .clock_widget import ClockWidget
from .log_form_widget import LogFormWidget
from .contact_table_widget import ContactTableWidget
from .header_widget import HeaderWidget
from .contact_queue_widget import ContactQueueWidget


class LogContestView(QWidget):
    def __init__(self, parent=None, callsign="", log_type_name="Concurso", log_date=""):
        super().__init__(parent)
        self.callsign = callsign
        self.log_type_name = log_type_name
        self.log_date = log_date
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        # Header al inicio
        self.header_widget = HeaderWidget()
        self.header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.header_widget)
        # Fila horizontal: input de indicativo y área de info
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
        # Cola de contactos
        self.queue_widget = ContactQueueWidget(self)
        self.queue_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.queue_widget)
        # Formulario de log de concurso
        self.form_widget = LogFormWidget(
            self,
            log_type="contest",
            callsign=callsign,
            log_type_name=log_type_name,
            log_date=log_date,
        )
        self.form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.form_widget)
        # Relojes y botón de agregar contacto
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
        # Tabla de contactos
        self.table_widget = ContactTableWidget(self, log_type="contest")
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        # Conexiones y traducción
        translation_service.signal.language_changed.connect(self.retranslate_ui)
        self.callsign_info.suggestionSelected.connect(self._on_suggestion_selected)
        self.callsign_input.input.textChanged.connect(self.callsign_info.update_info)
        self.callsign_info.update_info(self.callsign_input.get_callsign())
        self.setLayout(layout)
        # Evitar foco en cola y tabla
        self.queue_widget.setFocusPolicy(Qt.NoFocus)
        self.table_widget.setFocusPolicy(Qt.NoFocus)
        self.callsign_info.setFocusPolicy(Qt.NoFocus)
        self.callsign_input.setFocusPolicy(Qt.NoFocus)
        self.header_widget.setFocusPolicy(Qt.NoFocus)
        self.form_widget.setFocusPolicy(Qt.NoFocus)
        # Refuerzo en hijos internos
        if hasattr(self.queue_widget, "queue_list"):
            self.queue_widget.queue_list.setFocusPolicy(Qt.NoFocus)
        if hasattr(self.table_widget, "table"):
            self.table_widget.table.setFocusPolicy(Qt.NoFocus)
        # Refuerzo en botones
        self.add_contact_btn.setFocusPolicy(Qt.StrongFocus)
        self.delete_contact_btn.setFocusPolicy(Qt.StrongFocus)
        # Orden de tabulación: input de indicativo -> RS_RX -> intercambio recibido -> RS_TX -> intercambio enviado -> observaciones -> botones
        if hasattr(self.form_widget, "rs_rx_input"):
            QWidget.setTabOrder(self.callsign_input.input, self.form_widget.rs_rx_input)
            QWidget.setTabOrder(
                self.form_widget.rs_rx_input, self.form_widget.exchange_received_input
            )
            QWidget.setTabOrder(
                self.form_widget.exchange_received_input, self.form_widget.rs_tx_input
            )
            QWidget.setTabOrder(
                self.form_widget.rs_tx_input, self.form_widget.exchange_sent_input
            )
            QWidget.setTabOrder(
                self.form_widget.exchange_sent_input,
                self.form_widget.observations_input,
            )
            QWidget.setTabOrder(
                self.form_widget.observations_input, self.add_contact_btn
            )
            QWidget.setTabOrder(self.add_contact_btn, self.delete_contact_btn)
        # Habilitar el botón de eliminar solo si hay una fila seleccionada
        self.table_widget.table.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_suggestion_selected(self, callsign):
        self.callsign_input.set_callsign(callsign)
        self.callsign_info.update_info(callsign)
        # Foco al primer campo del formulario de concurso
        if hasattr(self.form_widget, "exchange_received_input"):
            self.form_widget.exchange_received_input.setFocus()

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
        # Refresca el formato de fecha/hora de los relojes al cambiar idioma
        self.oa_clock.update_clock()
        self.utc_clock.update_clock()

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
        # Mostrar diálogo de confirmación
        from PySide6.QtWidgets import QMessageBox

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(translation_service.tr("delete_contact"))
        msg_box.setText(translation_service.tr("confirm_delete_contact"))
        msg_box.setInformativeText(
            f"{translation_service.tr('table_header_callsign')}: {callsign}"
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
        main_window = (
            self._find_main_window()
            if hasattr(self, "_find_main_window")
            else self.parent()
        )
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

    def _find_main_window(self):
        parent = self.parent()
        while parent:
            if parent.__class__.__name__ == "MainWindow":
                return parent
            parent = parent.parent()
        return None
