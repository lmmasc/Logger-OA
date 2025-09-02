from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QPushButton,
)
from PySide6.QtCore import Qt, QEvent
from interface_adapters.controllers.radio_operator_controller import (
    RadioOperatorController,
)
from translation.translation_service import translation_service
from config.settings_service import settings_service


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
        self.table.itemChanged.connect(self._on_item_changed)
        self._ignore_item_changed = False

    def _on_item_changed(self, item):
        """
        Handler para confirmar y guardar cambios en la base de datos o descartarlos.
        """
        if self._ignore_item_changed:
            return
        row = item.row()
        col = item.column()
        header = self.table.horizontalHeaderItem(col).text()
        callsign = self.table.item(
            row, 0
        ).text()  # Se asume que la columna 0 es el indicativo
        old_value = item.data(Qt.UserRole)
        new_value = item.text()
        yes_text = translation_service.tr("yes_button")
        no_text = translation_service.tr("no_button")
        box = QMessageBox(self)
        box.setWindowTitle(translation_service.tr("main_window_title"))
        box.setText(
            translation_service.tr("confirm_update_field").format(
                field=header, value=new_value
            )
        )
        yes_button = box.addButton(yes_text, QMessageBox.YesRole)
        no_button = box.addButton(no_text, QMessageBox.NoRole)
        box.setDefaultButton(no_button)
        box.exec()
        if box.clickedButton() == yes_button:
            # Actualizar en base de datos
            operator = next(
                (
                    op
                    for op in self.controller.list_operators()
                    if op.callsign == callsign
                ),
                None,
            )
            if operator:
                attr_map = {
                    translation_service.tr("name"): "name",
                    translation_service.tr("category"): "category",
                    translation_service.tr("type"): "type_",
                    translation_service.tr("district"): "district",
                    translation_service.tr("province"): "province",
                    translation_service.tr("department"): "department",
                    translation_service.tr("license"): "license_",
                    translation_service.tr("resolution"): "resolution",
                    translation_service.tr("expiration_date"): "expiration_date",
                    translation_service.tr("cutoff_date"): "cutoff_date",
                    translation_service.tr("enabled"): "enabled",
                    translation_service.tr("country"): "country",
                    translation_service.tr("updated_at"): "updated_at",
                }
                field = attr_map.get(header)
                if field:
                    # Convertir SI/NO a 1/0 si es el campo habilitado
                    if field == "enabled":
                        if new_value.strip().upper() in (
                            translation_service.tr("yes"),
                            "1",
                        ):
                            new_value = 1
                        else:
                            new_value = 0
                    setattr(operator, field, new_value)
                    self.controller.service.update_operator(operator)
        else:
            # Descartar el cambio visualmente
            self._ignore_item_changed = True
            item.setText(old_value if old_value is not None else "")
            self._ignore_item_changed = False

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
                    (
                        translation_service.tr("yes")
                        if op.enabled == 1
                        else translation_service.tr("no")
                    ),
                    op.country,
                    op.updated_at,
                ]
            ):
                item = QTableWidgetItem(str(value))
                # Guardar el valor original para poder restaurar si se cancela
                item.setData(Qt.UserRole, str(value))
                self.table.setItem(row_idx, col_idx, item)

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
        Actualiza el título y los encabezados de la tabla según el idioma actual, y traduce los valores de la columna 'habilitado'.
        """
        self.setWindowTitle(translation_service.tr("db_table"))
        headers = self.get_translated_headers()
        self.table.setHorizontalHeaderLabels(headers)
        # Buscar el índice de la columna 'habilitado' de forma robusta
        try:
            enabled_col = headers.index(translation_service.tr("enabled"))
        except ValueError:
            enabled_col = None
        if enabled_col is not None:
            for row in range(self.table.rowCount()):
                item = self.table.item(row, enabled_col)
                if item:
                    val = item.text().strip().upper()
                    if val in ("1", "SI", "YES"):  # Puede venir de distintas formas
                        item.setText(translation_service.tr("yes"))
                    else:
                        item.setText(translation_service.tr("no"))

    def showEvent(self, event):
        """
        Restaura el ancho de las columnas al mostrar la ventana.
        """
        super().showEvent(event)
        widths = settings_service.get_value("db_table_column_widths", None)
        if widths:
            for i, w in enumerate(widths):
                self.table.setColumnWidth(i, int(w))
        # Conectar señal solo una vez
        if not hasattr(self, "_resize_connected"):
            self.table.horizontalHeader().sectionResized.connect(
                self.save_column_widths
            )
            self._resize_connected = True

    def save_column_widths(self, *args):
        """
        Guarda el ancho de las columnas en la configuración al ser redimensionadas.
        """
        widths = [self.table.columnWidth(i) for i in range(self.table.columnCount())]
        settings_service.set_value("db_table_column_widths", widths)

    def closeEvent(self, event):
        """
        Guarda el ancho de las columnas al cerrar la ventana.
        """
        self.save_column_widths()
        super().closeEvent(event)
