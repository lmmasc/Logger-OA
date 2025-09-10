from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from translation.translation_service import translation_service


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

    def set_columns(self):
        if self.log_type == "contest":
            headers = [
                translation_service.tr("table_header_callsign"),
                translation_service.tr("time"),
                translation_service.tr("exchange_received"),
                translation_service.tr("exchange_sent"),
                translation_service.tr("rs_rx"),
                translation_service.tr("rs_tx"),
            ]
        else:
            headers = [
                translation_service.tr("table_header_callsign"),
                translation_service.tr("name"),
                translation_service.tr("country"),
                translation_service.tr("station"),
                translation_service.tr("energy"),
                translation_service.tr("power"),
                translation_service.tr("rs_rx"),
                translation_service.tr("rs_tx"),
                translation_service.tr("clock_oa_label"),
                translation_service.tr("clock_utc_label"),
            ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def set_contacts(self, contacts):
        # ...eliminado debug print...
        # Define las claves esperadas según el tipo de log
        if self.log_type == "contest":
            keys = [
                "callsign",
                "qtr_utc",
                "exchange_received",
                "exchange_sent",
                "rs_rx",
                "rs_tx",
            ]
        else:
            keys = [
                "callsign",
                "name",
                "country",
                "station",
                "energy",
                "power",
                "rs_rx",
                "rs_tx",
                "qtr_oa",
                "qtr_utc",
            ]
        self.table.setRowCount(len(contacts))
        self.table.setColumnCount(len(keys))
        for row, contact in enumerate(contacts):
            # ...eliminado debug print...
            for col, key in enumerate(keys):
                value = contact.get(key, "")
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        self.table.viewport().update()

    def retranslate_ui(self):
        self.set_columns()
