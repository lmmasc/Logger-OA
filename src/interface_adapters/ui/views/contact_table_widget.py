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
                translation_service.tr("callsign"),
                translation_service.tr("time"),
                translation_service.tr("exchange_received"),
                translation_service.tr("exchange_sent"),
                translation_service.tr("rs_rx"),
                translation_service.tr("rs_tx"),
            ]
        else:
            headers = [
                translation_service.tr("callsign"),
                translation_service.tr("time"),
                translation_service.tr("station"),
                translation_service.tr("power"),
                translation_service.tr("rs_rx"),
                translation_service.tr("rs_tx"),
            ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def set_contacts(self, contacts):
        self.table.setRowCount(len(contacts))
        for row, contact in enumerate(contacts):
            for col, key in enumerate(contact.keys()):
                self.table.setItem(row, col, QTableWidgetItem(str(contact[key])))

    def retranslate_ui(self):
        self.set_columns()
