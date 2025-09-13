from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
from translation.translation_service import translation_service
from config.settings_service import settings_service
from PySide6.QtCore import Qt


class ContactTableWidget(QWidget):
    """
    Widget para mostrar la tabla de contactos agregados al log actual.
    Adaptable para operativos y concursos.
    """

    def __init__(self, parent=None, log_type="ops"):
        super().__init__(parent)
        self.log_type = log_type
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.set_columns()
        # Persistencia de anchos de columna diferenciada por tipo de log
        self._column_widths_key = f"contact_table_column_widths_{self.log_type}"
        self.table.horizontalHeader().sectionResized.connect(self.save_column_widths)
        self.load_column_widths()
        # Deshabilitar edición directa
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Conectar doble clic a método personalizado
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        # Evitar que la tabla reciba el foco por tabulación si no es interactiva
        self.table.setFocusPolicy(Qt.NoFocus)

    def _on_item_double_clicked(self, item):
        """
        Abre el diálogo de edición para el contacto seleccionado, respetando traducción y tipos.
        """
        row = item.row()
        if not hasattr(self, "_last_contacts") or row >= len(self._last_contacts):
            return
        contact = self._last_contacts[row]
        # Importar y mostrar el diálogo de edición de contacto
        from interface_adapters.ui.dialogs.contact_edit_dialog import ContactEditDialog
        from PySide6.QtWidgets import QDialog

        dlg = ContactEditDialog(contact, self.log_type, self)
        if dlg.exec() == QDialog.Accepted and dlg.result_contact:
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
            if (
                not main_window
                or not hasattr(main_window, "current_log")
                or not main_window.current_log
            ):
                return
            db_path = getattr(main_window.current_log, "db_path", None)
            log_id = getattr(main_window.current_log, "id", None)
            contact_id = contact.get("id", None)
            contact_type = "operativo" if self.log_type == "ops" else "concurso"
            update_contact_in_log(
                db_path, log_id, contact_id, updated_data, contact_type
            )
            repo = ContactLogRepository(db_path)
            contacts = repo.get_contacts(log_id)
            main_window.current_log.contacts = contacts
            self.set_contacts(contacts)

    def set_columns(self):
        if self.log_type == "contest":
            headers = [
                translation_service.tr("table_header_callsign"),
                translation_service.tr("name"),
                translation_service.tr("region"),
                "QTR",
                translation_service.tr("rs_rx"),
                translation_service.tr("table_header_exchange_rx"),
                translation_service.tr("rs_tx"),
                translation_service.tr("table_header_exchange_tx"),
                translation_service.tr("observations"),
            ]
        else:
            headers = [
                translation_service.tr("table_header_callsign"),
                translation_service.tr("name"),
                translation_service.tr("country"),
                translation_service.tr("region"),
                translation_service.tr("station"),
                translation_service.tr("energy"),
                translation_service.tr("table_header_power"),
                translation_service.tr("rs_rx"),
                translation_service.tr("rs_tx"),
                translation_service.tr("clock_oa_label"),
                translation_service.tr("clock_utc_label"),
                translation_service.tr("observations"),
            ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def set_contacts(self, contacts):
        self._last_contacts = contacts
        # Define las claves esperadas según el tipo de log
        if self.log_type == "contest":
            keys = [
                "callsign",
                "name",
                "region",
                "qtr_oa",
                "rs_rx",
                "exchange_received",
                "rs_tx",
                "exchange_sent",
                "observations",
            ]
        else:
            keys = [
                "callsign",
                "name",
                "country",
                "region",
                "station",
                "energy",
                "power",
                "rs_rx",
                "rs_tx",
                "qtr_oa",
                "qtr_utc",
                "obs",
            ]
        self.table.setRowCount(len(contacts))
        self.table.setColumnCount(len(keys))
        import datetime

        lang = translation_service.get_language()
        if lang == "es":
            date_fmt = "%d/%m/%Y"
        else:
            date_fmt = "%m/%d/%Y"

        for row, contact in enumerate(contacts):
            for col, key in enumerate(keys):
                if key == "qtr_oa":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        dt_utc = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        )
                        dt_oa = dt_utc - datetime.timedelta(hours=5)
                        if self.log_type == "contest":
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
                    value = translation_service.tr(contact.get(key, ""))
                elif key == "power":
                    val = contact.get(key, "")
                    value = f"{val} W" if val else ""
                elif self.log_type == "contest" and key in (
                    "exchange_received",
                    "exchange_sent",
                ):
                    val = contact.get(key, "")
                    value = str(val).zfill(3) if val else ""
                else:
                    value = contact.get(key, "")
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        self.table.viewport().update()

    def retranslate_ui(self):
        self.set_columns()
        # Recarga los datos si existen
        if hasattr(self, "_last_contacts"):
            self.set_contacts(self._last_contacts)

    def save_column_widths(self, *args):
        """
        Guarda los anchos de columna, evitando sobrescribir con 0 y manteniendo el último valor válido.
        """
        prev_widths = settings_service.get_value(self._column_widths_key, None)
        if prev_widths is None:
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
        if widths:
            for i, w in enumerate(widths):
                if int(w) == 0:
                    w = 100
                self.table.setColumnWidth(i, int(w))
