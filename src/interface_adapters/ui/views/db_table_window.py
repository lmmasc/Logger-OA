# --- Imports estándar ---
from functools import partial

# --- Imports de terceros ---
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
    QGridLayout,  # Para grid de checkboxes
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontDatabase
from utils.resources import get_resource_path

# --- Imports de la aplicación ---
from interface_adapters.controllers.radio_operator_controller import (
    RadioOperatorController,
)
from translation.translation_service import translation_service
from config.settings_service import settings_service
from utils.text import filter_text_match


class DBTableWindow(QWidget):
    """
    Ventana principal para la gestión y visualización de la tabla de operadores.
    Permite filtrar, editar, agregar y eliminar operadores, con persistencia de configuración y soporte multilenguaje.
    """

    COLUMNS = [
        {"key": "callsign", "translation": "db_table_header_callsign"},
        {"key": "name", "translation": "db_table_header_name"},
        {"key": "category", "translation": "db_table_header_category"},
        {"key": "type", "translation": "db_table_header_type"},
        {"key": "country", "translation": "db_table_header_country"},
        {"key": "region", "translation": "db_table_header_region"},
        {"key": "department", "translation": "db_table_header_department"},
        {"key": "province", "translation": "db_table_header_province"},
        {"key": "district", "translation": "db_table_header_district"},
        {"key": "license", "translation": "db_table_header_license"},
        {"key": "resolution", "translation": "db_table_header_resolution"},
        {"key": "expiration_date", "translation": "db_table_header_expiration_date"},
        {"key": "cutoff_date", "translation": "db_table_header_cutoff_date"},
        {"key": "enabled", "translation": "db_table_header_enabled"},
        {"key": "updated_at", "translation": "db_table_header_updated_at"},
    ]

    # --- Inicialización y eventos principales ---
    def __init__(self, parent=None):
        """
        Inicializa la ventana de la tabla de operadores, crea la UI, checkboxes de visibilidad,
        filtro, y conecta señales para persistencia y edición.
        """
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("db_table"))
        self.setWindowFlag(Qt.WindowType.Window)
        self.resize(1200, 700)

        # Estado de paginación y filtro
        self._page_size = 500
        self._current_page = 0
        self._total_count = 0
        self._filter_timer = QTimer(self)
        self._filter_timer.setSingleShot(True)
        self._filter_timer.setInterval(180)
        self._filter_timer.timeout.connect(self._apply_filter_debounced)

        main_layout = QVBoxLayout()

        # Filtro y métricas
        filter_layout = QHBoxLayout()
        self.filter_edit = QLineEdit()
        font_path = get_resource_path("assets/RobotoMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font = self.filter_edit.font()
        if font_families:
            font.setFamily(font_families[0])
        else:
            font.setFamily("Monospace")
        font.setPointSize(16)
        font.setBold(True)
        self.filter_edit.setFont(font)
        self.filter_edit.setPlaceholderText(
            translation_service.tr("filter_placeholder")
        )
        self.filter_edit.textChanged.connect(self._normalize_filter_text)
        self.filter_column_combo = QComboBox()
        self.filter_column_combo.setFixedWidth(150)
        self.filter_label = QLabel(translation_service.tr("filter_by"))
        self.filter_label.setFixedWidth(130)
        self.filter_results_label = QLabel(translation_service.tr("filter_results"))
        self.filter_results_count = QLabel("0")
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_edit)
        filter_layout.addWidget(self.filter_column_combo)
        filter_layout.addWidget(self.filter_results_label)
        filter_layout.addWidget(self.filter_results_count)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Tabla
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        # Controlador
        self.controller = RadioOperatorController()

        # Checkboxes de visibilidad de columnas (grid 2 filas)
        self.checkbox_layout = QGridLayout()
        self.column_checkboxes = []
        self.headers = self.get_translated_headers()
        # Inicializar el selector de columna de filtro solo una vez
        self.filter_column_combo.addItems(self.headers)
        # Restaurar selección previa de columna de filtro
        try:
            raw_prev = settings_service.get_value("db_table_filter_col_index", "0")
            prev_idx = int(str(raw_prev))
        except Exception:
            prev_idx = 0
        if self.filter_column_combo.count():
            self.filter_column_combo.setCurrentIndex(
                min(max(prev_idx, 0), self.filter_column_combo.count() - 1)
            )
        column_keys = [col["key"] for col in self.COLUMNS]
        col_visible = settings_service.get_value("db_table_column_visible_dict", None)
        if not col_visible or not isinstance(col_visible, dict):
            col_visible = {k: True for k in column_keys}
        num_cols = len(column_keys)
        split = num_cols // 2 + num_cols % 2
        for idx, coldef in enumerate(self.COLUMNS):
            key = coldef["key"]
            cb = QCheckBox(self.headers[idx])
            cb.setObjectName(key)
            cb.setChecked(bool(col_visible.get(key, True)))
            cb.stateChanged.connect(partial(self.toggle_column, idx))
            self.column_checkboxes.append(cb)
            row = 0 if idx < split else 1
            col = idx if row == 0 else idx - split
            self.checkbox_layout.addWidget(cb, row, col)
        self.checkbox_layout.setRowStretch(0, 1)
        self.checkbox_layout.setRowStretch(1, 1)
        main_layout.insertLayout(1, self.checkbox_layout)

        # Controles de paginación
        self.pagination_layout = QHBoxLayout()
        self.btn_prev = QPushButton("◀")
        self.btn_next = QPushButton("▶")
        self.page_info = QLabel("")
        self.btn_prev.clicked.connect(self._on_prev_page)
        self.btn_next.clicked.connect(self._on_next_page)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.btn_prev)
        self.pagination_layout.addWidget(self.page_info)
        self.pagination_layout.addWidget(self.btn_next)
        self.pagination_layout.addStretch()
        main_layout.addLayout(self.pagination_layout)

        # Final de layout
        self.setLayout(main_layout)

        # Flags internos
        self._ignore_item_changed = False
        self._updating_ui = False

        # Cargar datos iniciales y conectar eventos de filtro
        self.load_data()
        self.filter_edit.textChanged.connect(self.apply_filter)
        self.filter_column_combo.currentIndexChanged.connect(
            self._on_filter_column_changed
        )
        # Conectar señal para guardar anchos de columnas al redimensionar
        self.table.horizontalHeader().sectionResized.connect(self.save_column_widths)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )  # Corrige enum para Pylance
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)

        # Botones para agregar y eliminar operador
        btn_add = QPushButton(translation_service.tr("add_operator"))
        btn_add.setObjectName("AddOperatorButton")
        btn_add.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        btn_add.clicked.connect(self._on_add_operator)
        self.btn_add = btn_add

        btn_delete = QPushButton(translation_service.tr("delete_operator"))
        btn_delete.setObjectName("DeleteOperatorButton")
        btn_delete.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        btn_delete.setEnabled(False)
        btn_delete.clicked.connect(self._on_delete_operator)
        self.btn_delete = btn_delete

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(btn_add)
        btns_layout.addWidget(btn_delete)
        main_layout.insertLayout(0, btns_layout)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)

    # --- Métodos de UI y traducción ---
    def retranslate_ui(self):
        """
        Actualiza los textos de la UI y los headers según el idioma actual.
        """
        # Actualizar label y placeholder del filtro
        if hasattr(self, "filter_label"):
            self.filter_label.setText(translation_service.tr("filter_by"))
        if hasattr(self, "filter_edit"):
            self.filter_edit.setPlaceholderText(
                translation_service.tr("filter_placeholder")
            )
        if hasattr(self, "filter_results_label"):
            self.filter_results_label.setText(translation_service.tr("filter_results"))
        # Actualizar label y placeholder del filtro
        if hasattr(self, "filter_label"):
            self.filter_label.setText(translation_service.tr("filter_by"))
        if hasattr(self, "filter_edit"):
            self.filter_edit.setPlaceholderText(
                translation_service.tr("filter_placeholder")
            )
        """
        Actualiza los textos de la UI y los headers según el idioma actual.
        """
        self._updating_ui = True
        self.setWindowTitle(translation_service.tr("db_table"))
        self.headers = self.get_translated_headers()
        self.table.setHorizontalHeaderLabels(self.headers)
        # Preservar selección del combo al retraducir
        prev_index = (
            self.filter_column_combo.currentIndex()
            if self.filter_column_combo.count()
            else 0
        )
        self.filter_column_combo.blockSignals(True)
        self.filter_column_combo.clear()
        self.filter_column_combo.addItems(self.headers)
        if self.filter_column_combo.count():
            self.filter_column_combo.setCurrentIndex(
                min(max(prev_index, 0), self.filter_column_combo.count() - 1)
            )
        self.filter_column_combo.blockSignals(False)
        # Actualizar texto de los botones de agregar y eliminar operador
        if hasattr(self, "btn_add"):
            self.btn_add.setText(translation_service.tr("add_operator"))
        if hasattr(self, "btn_delete"):
            self.btn_delete.setText(translation_service.tr("delete_operator"))
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
        return [translation_service.tr(col["translation"]) for col in self.COLUMNS]

    # --- Métodos de visibilidad y checkboxes ---
    def toggle_column(self, col, state):
        """
        Cambia la visibilidad de una columna según el checkbox correspondiente y guarda el estado.
        """
        if self._updating_ui:
            return
        column_keys = [col["key"] for col in self.COLUMNS]
        key = column_keys[col]
        col_visible = settings_service.get_value("db_table_column_visible_dict", None)
        if not col_visible or not isinstance(col_visible, dict):
            col_visible = {k: True for k in column_keys}
        for idx, key in enumerate(column_keys):
            col_visible[key] = self.column_checkboxes[idx].isChecked()
        settings_service.set_value("db_table_column_visible_dict", col_visible)
        self.apply_column_visibility()

    def apply_column_visibility(self):
        """
        Aplica la visibilidad de columnas según el estado de los checkboxes.
        """
        column_keys = [col["key"] for col in self.COLUMNS]
        if self.table.columnCount() != len(self.column_checkboxes):
            return
        vis_states = {}
        for idx, cb in enumerate(self.column_checkboxes):
            self.table.setColumnHidden(idx, not cb.isChecked())
            vis_states[column_keys[idx]] = cb.isChecked()

    # --- Métodos de filtro ---
    def apply_filter(self):
        """
        Dispara filtro con debounce; la aplicación real recarga desde DB con WHERE/LIKE.
        """
        self._filter_timer.start()

    def _apply_filter_debounced(self):
        # Reiniciar a primera página al cambiar el filtro o columna
        self._current_page = 0
        self.load_data()

    def _on_filter_column_changed(self, idx: int):
        # Guardar índice seleccionado y aplicar filtro con debounce
        try:
            settings_service.set_value("db_table_filter_col_index", int(idx))
        except Exception:
            pass
        self.apply_filter()

    # --- Métodos de datos y edición ---
    def load_data(self):
        """
        Carga los datos de operadores en la tabla, aplica headers, visibilidad y anchos.
        """
        self._updating_ui = True
        self.table.blockSignals(True)
        # Obtener filtro actual
        column_keys = [col["key"] for col in self.COLUMNS]
        filter_col_key = (
            column_keys[self.filter_column_combo.currentIndex()]
            if self.filter_column_combo.count()
            else "callsign"
        )
        filter_text = self.filter_edit.text().strip()
        # Cargar datos paginados desde el controlador
        operators, total = self.controller.list_operators_paged(
            page=self._current_page,
            page_size=self._page_size,
            order_by="callsign",
            asc=True,
            filter_col=filter_col_key,
            filter_text=filter_text,
        )
        self._total_count = total
        headers = self.headers
        if not operators:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.setHorizontalHeaderLabels([])
            self._updating_ui = False
            self.table.blockSignals(False)
            # Actualizar paginación aunque no haya datos
            self._update_pagination_info()
            return
        self.table.setRowCount(len(operators))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        # No tocar el combo del filtro aquí para no resetear selección ni disparar señales
        column_keys = [col["key"] for col in self.COLUMNS]

        from utils.datetime import format_iso_date, format_iso_datetime
        from domain.callsign_utils import get_country_full_name
        from utils.text import normalize_ascii

        # Detectar idioma actual correctamente
        lang = "es"
        if hasattr(translation_service, "get_language"):
            lang_enum = translation_service.get_language()
            lang = getattr(lang_enum, "value", str(lang_enum))

        for row_idx, op in enumerate(operators):
            for col_idx, key in enumerate(column_keys):
                if key == "enabled":
                    display = (
                        translation_service.tr("yes")
                        if op.enabled == 1
                        else translation_service.tr("no")
                    )
                    item = QTableWidgetItem(display)
                elif key in ("expiration_date", "cutoff_date"):
                    value = getattr(op, key, "")
                    date_str = format_iso_date(value)
                    if date_str:
                        parts = date_str.split("-")
                        display_date = f"{parts[2]}/{parts[1]}/{parts[0]}"
                    else:
                        display_date = ""
                    item = QTableWidgetItem(display_date)
                elif key == "updated_at":
                    value = getattr(op, key, "")
                    dt_str = format_iso_datetime(value)
                    if dt_str:
                        date_part, time_part = dt_str.split(" ")
                        y, m, d = date_part.split("-")
                        display_dt = f"{time_part} {d}/{m}/{y}"
                    else:
                        display_dt = ""
                    item = QTableWidgetItem(display_dt)
                elif key == "country":
                    itu_code = normalize_ascii(getattr(op, "country", "")).upper()
                    country_name = get_country_full_name(itu_code, lang)
                    if country_name:
                        display_country = normalize_ascii(country_name).upper()
                    else:
                        display_country = itu_code
                    item = QTableWidgetItem(display_country)
                else:
                    attr = (
                        "type_"
                        if key == "type"
                        else ("license_" if key == "license" else key)
                    )
                    value = getattr(op, attr, "")
                    item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)
        self.apply_column_visibility()
        # Actualizar contador y paginación
        if hasattr(self, "filter_results_count"):
            self.filter_results_count.setText(str(self._total_count))
        self._update_pagination_info()
        # --- ANCHOS DE COLUMNA ---
        widths = settings_service.get_value("db_table_column_widths", None)
        # Validación para settings_service.get_value (anchos de columna)
        if isinstance(widths, list):
            for i, w in enumerate(widths):
                if int(w) == 0:
                    widths[i] = 100
            for i, w in enumerate(widths):
                self.table.setColumnWidth(i, int(w))
        self._updating_ui = False
        self.table.blockSignals(False)

    def _on_prev_page(self):
        if self._current_page > 0:
            if hasattr(self, "_filter_timer"):
                self._filter_timer.stop()
            self._current_page -= 1
            self.load_data()

    def _on_next_page(self):
        max_page = (
            (self._total_count - 1) // self._page_size if self._total_count > 0 else 0
        )
        if self._current_page < max_page:
            if hasattr(self, "_filter_timer"):
                self._filter_timer.stop()
            self._current_page += 1
            self.load_data()

    def _update_pagination_info(self):
        max_page = (
            (self._total_count - 1) // self._page_size if self._total_count > 0 else 0
        )
        self.page_info.setText(
            f" {self._current_page + 1} / {max_page + 1}  ·  {self._total_count}"
        )
        self.btn_prev.setEnabled(self._current_page > 0)
        self.btn_next.setEnabled(self._current_page < max_page)

    def _on_item_double_clicked(self, item):
        """
        Abre el diálogo de edición para el registro seleccionado.
        """
        row = item.row()
        callsign_item = self.table.item(row, 0)
        callsign = callsign_item.text() if callsign_item else ""
        # Evitar cargar toda la base: obtener por callsign
        operator = self.controller.get_operator_by_callsign(callsign)
        if operator:
            from interface_adapters.ui.dialogs.operator_edit_dialog import (
                OperatorEditDialog,
            )

            dlg = OperatorEditDialog(operator, self)
            if dlg.exec() == QDialog.DialogCode.Accepted and dlg.result_operator:
                # Actualizar el operador en la base de datos
                for k, v in dlg.result_operator.items():
                    setattr(operator, k if k != "type" else "type_", v)
                self.controller.service.update_operator(operator)
                self.load_data()

    def _on_add_operator(self):
        """
        Abre el diálogo de alta manual de operador y agrega el registro si es válido.
        """
        from interface_adapters.ui.dialogs.operator_edit_dialog import (
            OperatorEditDialog,
        )
        from PySide6.QtWidgets import QDialog

        dlg = OperatorEditDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.result_operator:
            # Crear nuevo operador y guardar
            op_data = dlg.result_operator
            from domain.entities.radio_operator import RadioOperator

            # Mapear 'license' a 'license_' y 'type' a 'type_' para el constructor
            op_data_fixed = {}
            for k, v in op_data.items():
                if k == "license":
                    op_data_fixed["license_"] = v
                elif k == "type":
                    op_data_fixed["type_"] = v
                else:
                    op_data_fixed[k] = v
            new_op = RadioOperator(**op_data_fixed)
            self.controller.service.add_operator(new_op)
            self.load_data()

    def _on_selection_changed(self):
        """
        Habilita o deshabilita el botón de eliminar según si hay una fila seleccionada en la tabla de operadores.
        """
        selected_rows = self.table.selectionModel().selectedRows()
        self.btn_delete.setEnabled(len(selected_rows) == 1)

    def _on_delete_operator(self):
        """
        Elimina el operador seleccionado tras confirmación del usuario y actualización en la base de datos.
        """
        selected = self.table.selectedItems()
        if not selected:
            return
        row = selected[0].row()
        # Validación para .text() en tabla
        callsign_item = self.table.item(row, 0)
        callsign = callsign_item.text() if callsign_item else ""
        name_item = self.table.item(row, 1)
        name = name_item.text() if name_item else ""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle(translation_service.tr("delete_operator"))
        msg_box.setText(translation_service.tr("confirm_delete_operator"))
        msg_box.setInformativeText(
            f"{translation_service.tr('db_table_header_callsign')}: {callsign}\n{translation_service.tr('db_table_header_name')}: {name}"
        )
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.button(QMessageBox.StandardButton.Yes).setText(
            translation_service.tr("yes_button")
        )
        msg_box.button(QMessageBox.StandardButton.No).setText(
            translation_service.tr("no_button")
        )
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.service.delete_operator_by_callsign(callsign)
            self.load_data()

    # --- Persistencia de anchos de columna ---
    def save_column_widths(self, *args):
        """
        Guarda los anchos de columna, evitando sobrescribir con 0 y manteniendo el último valor válido.
        """
        # Validación para settings_service.get_value (save_column_widths)
        prev_widths = settings_service.get_value("db_table_column_widths", None)
        if not isinstance(prev_widths, list):
            prev_widths = [100] * self.table.columnCount()
        widths = []
        for i in range(self.table.columnCount()):
            w = self.table.columnWidth(i)
            if w == 0:
                if prev_widths and i < len(prev_widths):
                    widths.append(prev_widths[i])
                else:
                    widths.append(100)
            else:
                widths.append(w)
        settings_service.set_value("db_table_column_widths", widths)

    def _normalize_filter_text(self, text):
        """
        Normaliza el texto del filtro a mayúsculas y mantiene la posición del cursor.
        """
        cursor_pos = self.filter_edit.cursorPosition()
        upper_text = text.upper()
        if text != upper_text:
            self.filter_edit.blockSignals(True)
            self.filter_edit.setText(upper_text)
            self.filter_edit.setCursorPosition(cursor_pos)
            self.filter_edit.blockSignals(False)
