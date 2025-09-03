from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QDateEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt, QDate
from translation.translation_service import translation_service


class OperatorEditDialog(QDialog):
    def __init__(self, operator=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(
            translation_service.tr("edit_operator")
            if operator
            else translation_service.tr("add_operator")
        )
        self.setModal(True)
        self.setMinimumSize(
            500, 500
        )  # Tamaño mínimo recomendado para evitar textos cortados
        self.operator = operator
        self.result_operator = None
        self._setup_ui()
        if operator:
            self._load_operator(operator)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.inputs = {}
        # Campos básicos
        fields = [
            ("callsign", QLineEdit),
            ("name", QLineEdit),
            ("category", QComboBox),
            ("type", QComboBox),  # Cambiado a QComboBox
            ("district", QLineEdit),
            ("province", QLineEdit),
            ("department", QLineEdit),
            ("license", QLineEdit),
            ("resolution", QLineEdit),
            ("expiration_date", QDateEdit),
            ("cutoff_date", QDateEdit),
            ("enabled", QComboBox),
            ("country", QLineEdit),
        ]
        for key, widget_cls in fields:
            row = QHBoxLayout()
            label = QLabel(translation_service.tr(f"table_header_{key}"))
            row.addWidget(label)
            if widget_cls == QLineEdit:
                widget = QLineEdit()
                # Forzar mayúsculas en tiempo real
                widget.textChanged.connect(
                    lambda text, w=widget: (
                        w.setText(text.upper()) if text != text.upper() else None
                    )
                )
            elif widget_cls == QComboBox:
                widget = QComboBox()
                if key == "category":
                    widget.addItems(["NOVICIO", "INTERMEDIO", "SUPERIOR", "NO_APLICA"])
                elif key == "type":
                    widget.addItems(["OPERADOR", "INSTALADOR/OPERADOR", "NO_APLICA"])
                elif key == "enabled":
                    widget.addItems(
                        [translation_service.tr("yes"), translation_service.tr("no")]
                    )
            elif widget_cls == QDateEdit:
                widget = QDateEdit()
                widget.setDisplayFormat("dd/MM/yyyy")
                widget.setCalendarPopup(True)
            row.addWidget(widget)
            self.inputs[key] = widget
            layout.addLayout(row)
        # Botones
        btns = QHBoxLayout()
        self.btn_ok = QPushButton(translation_service.tr("yes_button"))
        self.btn_cancel = QPushButton(translation_service.tr("no_button"))
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def _load_operator(self, op):
        self.inputs["callsign"].setText(getattr(op, "callsign", "").upper())
        self.inputs["name"].setText(getattr(op, "name", "").upper())
        cat = getattr(op, "category", "NOVICIO")
        idx = self.inputs["category"].findText(cat)
        self.inputs["category"].setCurrentIndex(idx if idx >= 0 else 0)
        # type como combo
        type_val = getattr(op, "type_", "OPERADOR")
        idx_type = self.inputs["type"].findText(type_val)
        self.inputs["type"].setCurrentIndex(idx_type if idx_type >= 0 else 0)
        self.inputs["district"].setText(getattr(op, "district", "").upper())
        self.inputs["province"].setText(getattr(op, "province", "").upper())
        self.inputs["department"].setText(getattr(op, "department", "").upper())
        self.inputs["license"].setText(getattr(op, "license_", "").upper())
        self.inputs["resolution"].setText(getattr(op, "resolution", "").upper())
        # Fechas
        for key in ("expiration_date", "cutoff_date"):
            val = getattr(op, key, "")
            if val:
                try:
                    d, m, y = map(int, val.split("/"))
                    self.inputs[key].setDate(QDate(y, m, d))
                except Exception:
                    pass
        # Enabled
        enabled = getattr(op, "enabled", 1)
        self.inputs["enabled"].setCurrentIndex(0 if enabled == 1 else 1)
        self.inputs["country"].setText(getattr(op, "country", "").upper())

    def get_operator_data(self):
        # Devuelve un dict con los datos ingresados/validados
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                data[key] = widget.text().strip().upper()
            elif isinstance(widget, QComboBox):
                if key == "enabled":
                    data[key] = 1 if widget.currentIndex() == 0 else 0
                else:
                    data[key] = widget.currentText()
            elif isinstance(widget, QDateEdit):
                data[key] = widget.date().toString("dd/MM/yyyy")
        return data

    def accept(self):
        # Validar campos obligatorios y formato
        callsign = self.inputs["callsign"].text().strip()
        name = self.inputs["name"].text().strip()
        if not callsign:
            QMessageBox.warning(
                self, self.windowTitle(), translation_service.tr("callsign_required")
            )
            return
        if not name:
            QMessageBox.warning(
                self, self.windowTitle(), translation_service.tr("name_required")
            )
            return
        # Validar categoría
        if self.inputs["category"].currentText() not in (
            "NOVICIO",
            "INTERMEDIO",
            "SUPERIOR",
            "NO_APLICA",
        ):
            QMessageBox.warning(
                self, self.windowTitle(), translation_service.tr("invalid_category")
            )
            return
        # TODO: Validar fechas y otros campos si es necesario
        self.result_operator = self.get_operator_data()
        super().accept()
