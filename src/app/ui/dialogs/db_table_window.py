from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from app.db.queries import fetch_all
from app.utils.file_manager import get_db_path
from app.translation import tr


class DBTableWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 700)  # Tamaño inicial, no fijo
        self.setWindowTitle(tr("db_table"))
        self.setWindowFlag(Qt.Window)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        db_path = get_db_path()
        query = (
            "SELECT callsign, name, category, type, district, province, department, "
            "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at "
            "FROM radio_operators"
        )
        data = fetch_all(db_path, query)
        headers = [
            "Callsign",
            "Name",
            "Category",
            "Type",
            "District",
            "Province",
            "Department",
            "License",
            "Resolution",
            "Expiration Date",
            "Cutoff Date",
            "Enabled",
            "Country",
            "Updated At",
        ]
        if not data:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.setHorizontalHeaderLabels([])
            return
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # ...existing code...
