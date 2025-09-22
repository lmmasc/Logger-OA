# --- Imports de terceros ---
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
from PySide6.QtCore import Qt

# --- Imports de la aplicación ---
from translation.translation_service import translation_service
from config.settings_service import settings_service
from interface_adapters.ui.view_manager import LogType
from config.settings_service import LanguageValue


class ContactTableWidget(QWidget):
    """
    Widget para mostrar la tabla de contactos agregados al log actual.
    Adaptable para operativos y concursos.
    """

    def __init__(self, parent=None, log_type=LogType.OPERATION_LOG):
        """
        Inicializa el widget de la tabla de contactos, configura la UI y la persistencia de columnas.
        Args:
            parent: QWidget padre.
            log_type: Tipo de log (Enum LogType).
        """
        super().__init__(parent)
        self.log_type = log_type
        main_layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        self.set_columns()
        # Persistencia de anchos de columna diferenciada por tipo de log
        self._column_widths_key = f"contact_table_column_widths_{self.log_type.name}"
        self.table.horizontalHeader().sectionResized.connect(self.save_column_widths)
        self.load_column_widths()
        # Deshabilitar edición directa
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # Conectar doble clic a método personalizado
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        # Evitar que la tabla reciba el foco por tabulación si no es interactiva
        self.table.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        # Instalar eventFilter para detectar Tab
        self.table.installEventFilter(self)

    def eventFilter(self, obj, event):
        from PySide6.QtCore import QEvent, Qt

        if obj == self.table and event.type() == QEvent.KeyPress:  # type: ignore
            if event.key() == Qt.Key_F1:  # type: ignore  # F1 key
                parent = self.parent()
                while parent is not None:
                    callsign_input = getattr(parent, "callsign_input", None)
                    if callsign_input is not None and hasattr(callsign_input, "input"):
                        callsign_input.input.setFocus()
                        return True  # Evento consumido
                    parent = parent.parent()
        return super().eventFilter(obj, event)

    # Definición de columnas y claves de traducción diferenciadas
    LOG_CONTEST_COLUMNS = [
        {"key": "callsign", "translation": "log_contest_table_header_callsign"},
        {"key": "name", "translation": "log_contest_table_header_name"},
        {"key": "region", "translation": "log_contest_table_header_region"},
        {"key": "qtr_oa", "translation": "log_contest_table_header_qtr_oa"},
        {"key": "rs_rx", "translation": "log_contest_table_header_rs_rx"},
        {
            "key": "exchange_received",
            "translation": "log_contest_table_header_exchange_received",
        },
        {"key": "rs_tx", "translation": "log_contest_table_header_rs_tx"},
        {
            "key": "exchange_sent",
            "translation": "log_contest_table_header_exchange_sent",
        },
        {"key": "observations", "translation": "log_contest_table_header_observations"},
    ]
    LOG_OPERATIVE_COLUMNS = [
        {"key": "callsign", "translation": "log_operative_table_header_callsign"},
        {"key": "qtr_oa", "translation": "log_operative_table_header_qtr_oa"},
        {"key": "qtr_utc", "translation": "log_operative_table_header_qtr_utc"},
        {"key": "name", "translation": "log_operative_table_header_name"},
        {"key": "country", "translation": "log_operative_table_header_country"},
        {"key": "region", "translation": "log_operative_table_header_region"},
        {"key": "station", "translation": "log_operative_table_header_station"},
        {"key": "energy", "translation": "log_operative_table_header_energy"},
        {"key": "power", "translation": "log_operative_table_header_power"},
        {"key": "rs_rx", "translation": "log_operative_table_header_rs_rx"},
        {"key": "rs_tx", "translation": "log_operative_table_header_rs_tx"},
        {"key": "obs", "translation": "log_operative_table_header_obs"},
    ]

    def set_columns(self):
        """
        Configura los headers de la tabla según el tipo de log (operativo o concurso).
        """
        if self.log_type == LogType.CONTEST_LOG:
            headers = [
                translation_service.tr(col["translation"])
                for col in self.LOG_CONTEST_COLUMNS
            ]
        else:
            headers = [
                translation_service.tr(col["translation"])
                for col in self.LOG_OPERATIVE_COLUMNS
            ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def set_contacts(self, contacts):
        """
        Carga los contactos en la tabla y adapta los valores según el tipo de log y el idioma.
        Args:
            contacts: Lista de diccionarios con los datos de los contactos.
        """
        # Guardar los contactos en el orden original
        self._last_contacts = (
            contacts.copy() if isinstance(contacts, list) else list(contacts)
        )
        # Solo invertir para mostrar en la tabla
        display_contacts = list(reversed(contacts))
        # Define las claves esperadas según el tipo de log
        if self.log_type == LogType.CONTEST_LOG:
            keys = [col["key"] for col in self.LOG_CONTEST_COLUMNS]
        else:
            keys = [col["key"] for col in self.LOG_OPERATIVE_COLUMNS]
        self.table.setRowCount(len(display_contacts))
        self.table.setColumnCount(len(keys))
        import datetime

        lang = translation_service.get_language()
        if lang == LanguageValue.ES:
            date_fmt = "%d/%m"
        else:
            date_fmt = "%m/%d"

        # Numeración invertida: la fila superior tiene el número más alto
        total = len(display_contacts)
        for row, contact in enumerate(display_contacts):
            # Establecer el número de orden invertido en la primera columna
            item_num = QTableWidgetItem(str(total - row))
            self.table.setVerticalHeaderItem(row, item_num)
            for col, key in enumerate(keys):
                value = None
                if key == "qtr_oa":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        dt_utc = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        )
                        dt_oa = dt_utc - datetime.timedelta(hours=5)
                        if self.log_type == LogType.CONTEST_LOG:
                            value = dt_oa.strftime("%H:%M")
                        else:
                            value = dt_oa.strftime(f"%H:%M {date_fmt}")
                elif key == "qtr_utc":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        value = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        ).strftime(f"%H:%M {date_fmt}")
                elif key in ("station", "energy"):
                    val = contact.get(key, "")
                    if val == "no_data":  # Valor por defecto para "no data"
                        value = ""
                    else:
                        value = translation_service.tr(contact.get(key, ""))
                elif key == "power":
                    val = contact.get(key, "")
                    value = f"{val} W" if val else ""
                elif self.log_type == LogType.CONTEST_LOG and key in (
                    "exchange_received",
                    "exchange_sent",
                ):
                    val = contact.get(key, "")
                    value = str(val).zfill(3) if val else ""
                else:
                    value = contact.get(key, "")
                # --- Alineación derecha para RS_RX y RS_TX en concursos ---
                if self.log_type == LogType.CONTEST_LOG and key in ("rs_rx", "rs_tx"):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    self.table.setItem(row, col, item)
                else:
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
        self.table.viewport().update()
        self.table.repaint()
        self.table.hide()
        self.table.show()

    def retranslate_ui(self):
        """
        Actualiza los textos de la UI y refresca los datos de la tabla según el idioma actual.
        """
        self.set_columns()
        # El refresco de datos debe hacerse solo si se requiere por cambio de idioma,
        # y siempre con la lista actual de contactos.
        if hasattr(self, "_last_contacts") and self._last_contacts:
            self.set_contacts(self._last_contacts)

    def _on_item_double_clicked(self, item):
        """
        Abre el diálogo de edición para el contacto seleccionado, respetando traducción y tipos.
        """
        row = item.row()
        if not hasattr(self, "_last_contacts") or row >= len(self._last_contacts):
            return
            # La tabla muestra los contactos en orden invertido, así que el índice real es:
        real_index = len(self._last_contacts) - 1 - row
        if real_index < 0 or real_index >= len(self._last_contacts):
            return
        contact = self._last_contacts[real_index]
        # Importar y mostrar el diálogo de edición de contacto
        from interface_adapters.ui.dialogs.contact_edit_dialog import ContactEditDialog
        from PySide6.QtWidgets import QDialog
        from domain.contact_type import ContactType

        dlg = ContactEditDialog(contact, self.log_type, self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.result_contact:
            # Conservar id y timestamp originales
            updated_data = dlg.result_contact.copy()
            if "id" in contact:
                updated_data["id"] = contact["id"]
            # Actualizar el contacto usando caso de uso y refrescar tabla
            from application.use_cases.contact_management import update_contact_in_log
            from domain.repositories.contact_log_repository import ContactLogRepository

            main_window = self.parent()
            while main_window and main_window.__class__.__name__ != "MainWindow":
                main_window = main_window.parent()
            if not main_window or not hasattr(main_window, "current_log"):
                return
            current_log = getattr(main_window, "current_log", None)
            if not current_log:
                return
            db_path = getattr(current_log, "db_path", None)
            log_id = getattr(current_log, "id", None)
            contact_id = contact.get("id", None)
            contact_type = (
                ContactType.OPERATION
                if self.log_type == LogType.OPERATION_LOG
                else ContactType.CONTEST
            )
            if not db_path or not log_id:
                return
            update_contact_in_log(
                db_path, log_id, contact_id, updated_data, contact_type
            )
            repo = ContactLogRepository(db_path)
            contacts = repo.get_contacts(log_id)
            if hasattr(current_log, "contacts"):
                current_log.contacts = contacts
            self.set_contacts(contacts)
            # Replicar el flujo del botón: seleccionar celda superior, foco y scroll
            self.table.scrollToTop()

    def save_column_widths(self, *args):
        """
        Guarda los anchos de columna, evitando sobrescribir con 0 y manteniendo el último valor válido.
        """
        prev_widths = settings_service.get_value(self._column_widths_key, None)
        if not isinstance(prev_widths, list):
            prev_widths = [100] * self.table.columnCount()
        widths = []
        for i in range(self.table.columnCount()):
            w = self.table.columnWidth(i)
            if w == 0:
                if prev_widths and i < len(prev_widths):
                    widths.append(int(prev_widths[i]))
                else:
                    widths.append(100)
            else:
                widths.append(w)
        settings_service.set_value(self._column_widths_key, widths)

    def load_column_widths(self):
        """
        Carga los anchos de columna guardados y aplica protección de valores mínimos.
        """
        widths = settings_service.get_value(self._column_widths_key, None)
        if isinstance(widths, list):
            for i, w in enumerate(widths):
                if int(w) == 0:
                    w = 100
                self.table.setColumnWidth(i, int(w))
