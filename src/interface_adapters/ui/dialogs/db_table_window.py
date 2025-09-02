from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from interface_adapters.controllers.radio_operator_controller import (
    RadioOperatorController,
)
from translation.translation_service import translation_service


class DBTableWindow(QWidget):
    def __init__(self, parent=None):
        """
        Inicializa la ventana de tabla de operadores, configura el layout y carga los datos.
        """
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
        """
        Carga los operadores desde el controlador y actualiza la tabla con los datos y headers traducidos.
        """
        operators = self.controller.list_operators()
        # Ordenar por indicativo (callsign) antes de mostrar
        operators = sorted(operators, key=lambda op: op.callsign)
        headers = self.get_translated_headers()
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

    def get_translated_headers(self):
        """
        Devuelve la lista de encabezados traducidos para la tabla de operadores.
        """
        return [
            translation_service.tr("callsign"),
            translation_service.tr("name"),
            translation_service.tr("category"),
            translation_service.tr("type"),
            translation_service.tr("district"),
            translation_service.tr("province"),
            translation_service.tr("department"),
            translation_service.tr("license"),
            translation_service.tr("resolution"),
            translation_service.tr("expiration_date"),
            translation_service.tr("cutoff_date"),
            translation_service.tr("enabled"),
            translation_service.tr("country"),
            translation_service.tr("updated_at"),
        ]

    def retranslate_ui(self):
        """
        Actualiza el título y los encabezados de la tabla según el idioma actual.
        """
        self.setWindowTitle(translation_service.tr("db_table"))
        self.table.setHorizontalHeaderLabels(self.get_translated_headers())
