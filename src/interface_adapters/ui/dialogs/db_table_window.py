from functools import partial
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QLabel,
    QPushButton,
    QDialog,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from interface_adapters.controllers.radio_operator_controller import (
    RadioOperatorController,
)
from translation.translation_service import translation_service
from config.settings_service import settings_service


class DBTableWindow(QWidget):
    COLUMN_KEYS = [
        "callsign",
        "name",
        "category",
        "type",
        "district",
        "province",
        "department",
        "license",
        "resolution",
        "expiration_date",
        "cutoff_date",
        "enabled",
        "country",
        "updated_at",
    ]

    # --- Inicialización y eventos principales ---
    def __init__(self, parent=None):
        """
        Inicializa la ventana de la tabla de operadores, crea la UI, checkboxes de visibilidad,
        filtro, y conecta señales para persistencia y edición.
        """
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("db_table"))
        self.setWindowFlag(Qt.Window)
        self.resize(1200, 700)
        main_layout = QVBoxLayout()
        filter_layout = QHBoxLayout()
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            translation_service.tr("filter_placeholder")
        )
        self.filter_column_combo = QComboBox()
        self.filter_column_combo.setMinimumWidth(150)
        filter_label = QLabel(translation_service.tr("filter_by"))
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_edit)
        filter_layout.addWidget(self.filter_column_combo)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        self.controller = RadioOperatorController()
        self.setLayout(main_layout)
        self._ignore_item_changed = False
        self._updating_ui = False
        self.checkbox_layout = QHBoxLayout()
        self.column_checkboxes = []
        self.headers = self.get_translated_headers()
        col_visible = settings_service.get_value("db_table_column_visible_dict", None)
        if not col_visible or not isinstance(col_visible, dict):
            col_visible = {k: True for k in self.COLUMN_KEYS}
        col_visible["callsign"] = True
        col_visible["name"] = True
        for idx, key in enumerate(self.COLUMN_KEYS):
            cb = QCheckBox(self.headers[idx])
            cb.setObjectName(key)
            if idx in (0, 1):
                cb.setChecked(True)
                cb.setEnabled(False)
            else:
                cb.setChecked(bool(col_visible.get(key, True)))
                cb.stateChanged.connect(partial(self.toggle_column, idx))
            self.column_checkboxes.append(cb)
            self.checkbox_layout.addWidget(cb)
        self.checkbox_layout.addStretch()
        main_layout.insertLayout(1, self.checkbox_layout)
        self.load_data()
        self.filter_edit.textChanged.connect(self.apply_filter)
        self.filter_column_combo.currentIndexChanged.connect(self.apply_filter)
        # Conectar señal para guardar anchos de columnas al redimensionar
        self.table.horizontalHeader().sectionResized.connect(self.save_column_widths)
        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )  # Deshabilitar edición directa
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        # Botones para agregar y eliminar operador
        btns_layout = QHBoxLayout()
        btn_add = QPushButton(translation_service.tr("add_operator"))
        btn_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        btn_add.clicked.connect(self._on_add_operator)
        self.btn_add = btn_add
        btn_delete = QPushButton(translation_service.tr("delete_operator"))
        btn_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        btn_delete.setEnabled(False)
        btn_delete.clicked.connect(self._on_delete_operator)
        self.btn_delete = btn_delete
        btns_layout.addWidget(btn_add)
        btns_layout.addWidget(btn_delete)
        main_layout.insertLayout(0, btns_layout)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)

    # --- Métodos de UI y traducción ---
    def retranslate_ui(self):
        """
        Actualiza los textos de la UI y los headers según el idioma actual.
        """
        self._updating_ui = True
        self.setWindowTitle(translation_service.tr("db_table"))
        self.headers = self.get_translated_headers()
        self.table.setHorizontalHeaderLabels(self.headers)
        self.filter_column_combo.clear()
        self.filter_column_combo.addItems(self.headers)
        # Solo actualiza el texto de los checkboxes, sin recrearlos
        for idx, cb in enumerate(self.column_checkboxes):
            cb.blockSignals(True)
            cb.setText(self.headers[idx])
            cb.blockSignals(False)
        self._updating_ui = False
        self.apply_column_visibility()
        self.load_data()  # Recarga la tabla para asegurar traducción y sincronización

    def get_translated_headers(self):
        """
        Devuelve la lista de headers traducidos para la tabla y los checkboxes.
        """
        return [
            translation_service.tr(f"table_header_{key}") for key in self.COLUMN_KEYS
        ]

    # --- Métodos de visibilidad y checkboxes ---
    def toggle_column(self, col, state):
        """
        Cambia la visibilidad de una columna según el checkbox correspondiente y guarda el estado.
        """
        if self._updating_ui:
            return
        key = self.COLUMN_KEYS[col]
        col_visible = settings_service.get_value("db_table_column_visible_dict", None)
        if not col_visible or not isinstance(col_visible, dict):
            col_visible = {k: True for k in self.COLUMN_KEYS}
        for idx, key in enumerate(self.COLUMN_KEYS):
            col_visible[key] = self.column_checkboxes[idx].isChecked()
        settings_service.set_value("db_table_column_visible_dict", col_visible)
        self.apply_column_visibility()

    def apply_column_visibility(self):
        """
        Aplica la visibilidad de columnas según el estado de los checkboxes.
        """
        if self.table.columnCount() != len(self.column_checkboxes):
            return
        vis_states = {}
        for idx, cb in enumerate(self.column_checkboxes):
            self.table.setColumnHidden(idx, not cb.isChecked())
            vis_states[self.COLUMN_KEYS[idx]] = cb.isChecked()

    # --- Métodos de filtro ---
    def apply_filter(self):
        """
        Aplica el filtro de texto a la columna seleccionada en el combo.
        """
        text = self.filter_edit.text().strip().lower()
        col = self.filter_column_combo.currentIndex()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if not text:
                self.table.setRowHidden(row, False)
            else:
                value = item.text().strip().lower() if item else ""
                self.table.setRowHidden(row, text not in value)

    # --- Métodos de datos y edición ---
    def load_data(self):
        """
        Carga los datos de operadores en la tabla, aplica headers, visibilidad y anchos.
        """
        self._updating_ui = True
        self.table.blockSignals(True)
        operators = self.controller.list_operators()
        operators = sorted(operators, key=lambda op: op.callsign)
        headers = self.headers
        if not operators:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.setHorizontalHeaderLabels([])
            self.filter_column_combo.clear()
            self._updating_ui = False
            self.table.blockSignals(False)
            return
        self.table.setRowCount(len(operators))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.filter_column_combo.clear()
        self.filter_column_combo.addItems(headers)
        for row_idx, op in enumerate(operators):
            for col_idx, key in enumerate(self.COLUMN_KEYS):
                if key == "enabled":
                    display = (
                        translation_service.tr("yes")
                        if op.enabled == 1
                        else translation_service.tr("no")
                    )
                    item = QTableWidgetItem(display)
                else:
                    value = getattr(op, key if key != "type" else "type_", "")
                    item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)
        self.apply_column_visibility()
        self.apply_filter()
        # --- ANCHOS DE COLUMNA ---
        widths = settings_service.get_value("db_table_column_widths", None)
        if widths:
            # Si hay valores en 0, ponerlos en 100
            for i, w in enumerate(widths):
                if int(w) == 0:
                    widths[i] = 100
            for i, w in enumerate(widths):
                self.table.setColumnWidth(i, int(w))
        self._updating_ui = False
        self.table.blockSignals(False)

    def _on_item_double_clicked(self, item):
        """
        Abre el diálogo de edición para el registro seleccionado.
        """
        row = item.row()
        callsign = self.table.item(row, 0).text()
        operator = next(
            (op for op in self.controller.list_operators() if op.callsign == callsign),
            None,
        )
        if operator:
            from .operator_edit_dialog import OperatorEditDialog

            dlg = OperatorEditDialog(operator, self)
            if dlg.exec() == QDialog.Accepted and dlg.result_operator:
                # Actualizar el operador en la base de datos
                for k, v in dlg.result_operator.items():
                    setattr(operator, k if k != "type" else "type_", v)
                self.controller.service.update_operator(operator)
                self.load_data()

    def _on_add_operator(self):
        """
        Abre el diálogo de alta manual de operador y agrega el registro si es válido.
        """
        from .operator_edit_dialog import OperatorEditDialog
        from PySide6.QtWidgets import QDialog

        dlg = OperatorEditDialog(parent=self)
        if dlg.exec() == QDialog.Accepted and dlg.result_operator:
            # Crear nuevo operador y guardar
            op_data = dlg.result_operator
            Operator = (
                type(self.controller.list_operators()[0])
                if self.controller.list_operators()
                else None
            )
            if Operator:
                # Mapear 'license' a 'license_' y 'type' a 'type_' para el constructor
                op_data_fixed = {}
                for k, v in op_data.items():
                    if k == "license":
                        op_data_fixed["license_"] = v
                    elif k == "type":
                        op_data_fixed["type_"] = v
                    else:
                        op_data_fixed[k] = v
                new_op = Operator(**op_data_fixed)
                self.controller.service.add_operator(new_op)
                self.load_data()

    def _on_selection_changed(self):
        selected_rows = self.table.selectionModel().selectedRows()
        self.btn_delete.setEnabled(len(selected_rows) == 1)

    def _on_delete_operator(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        row = selected[0].row()
        callsign = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(translation_service.tr("delete_operator"))
        msg_box.setText(translation_service.tr("confirm_delete_operator"))
        msg_box.setInformativeText(
            f"{translation_service.tr('table_header_callsign')}: {callsign}\n{translation_service.tr('table_header_name')}: {name}"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText(translation_service.tr("yes_button"))
        msg_box.button(QMessageBox.No).setText(translation_service.tr("no_button"))
        reply = msg_box.exec()
        if reply == QMessageBox.Yes:
            self.controller.service.delete_operator_by_callsign(callsign)
            self.load_data()

    # --- Persistencia de anchos de columna ---
    def save_column_widths(self, *args):
        """
        Guarda los anchos de columna, evitando sobrescribir con 0 y manteniendo el último valor válido.
        """
        # Guardar solo si el ancho es >0, si no, mantener el último valor guardado
        prev_widths = settings_service.get_value("db_table_column_widths", None)
        if prev_widths is None:
            prev_widths = [100] * self.table.columnCount()
        widths = []
        for i in range(self.table.columnCount()):
            w = self.table.columnWidth(i)
            if w == 0:
                # Mantener el último valor guardado
                if prev_widths and i < len(prev_widths):
                    widths.append(prev_widths[i])
                else:
                    widths.append(100)
            else:
                widths.append(w)
        settings_service.set_value("db_table_column_widths", widths)
