from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from interface_adapters.controllers.radio_operator_controller import (
    RadioOperatorController,
)
from translation.translation_service import translation_service


class DBTableWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 700)  # Tamaño inicial, no fijo
        self.setWindowTitle(translation_service.tr("db_table"))
        self.setWindowFlag(Qt.Window)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.controller = RadioOperatorController()
        self.load_data()
        self.setLayout(layout)

    def load_data(self):
        operators = self.controller.list_operators()
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
        if not operators:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.setHorizontalHeaderLabels([])
            return
        self.table.setRowCount(len(operators))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        for row_idx, op in enumerate(operators):
            for col_idx, value in enumerate(
                [
                    op.callsign,
                    op.name,
                    op.category,
                    op.type_,
                    op.district,
                    op.province,
                    op.department,
                    op.license_,
                    op.resolution,
                    op.expiration_date,
                    op.cutoff_date,
                    op.enabled,
                    op.country,
                    op.updated_at,
                ]
            ):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
