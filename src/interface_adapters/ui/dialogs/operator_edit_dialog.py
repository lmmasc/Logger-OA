"""
OperatorEditDialog
Diálogo para editar o agregar operadores de radio.
Permite ingresar y validar los datos de un operador, incluyendo campos específicos para Perú y otros países.
"""

# --- Imports de terceros ---
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

# --- Imports de la aplicación ---
from translation.translation_service import translation_service
import datetime


class OperatorEditDialog(QDialog):
    """
    Diálogo para editar o agregar operadores de radio.
    Permite ingresar y validar los datos de un operador, incluyendo campos específicos para Perú y otros países.
    """

    def __init__(self, operator=None, parent=None):
        """
        Inicializa el diálogo de edición/agregado de operador.
        Args:
            operator (obj, opcional): Operador a editar. Si es None, se crea uno nuevo.
            parent (QWidget, opcional): Widget padre.
        """
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
        """
        Configura la interfaz de usuario y los campos del formulario.
        """
        layout = QVBoxLayout(self)
        self.inputs = {}
        self._peru_fields = [
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
        ]
        # Campos básicos (sin country)
        fields = [
            ("callsign", QLineEdit),
            ("name", QLineEdit),
            ("category", QComboBox),
            ("type", QComboBox),
            ("region", QLineEdit),  # Campo agregado para región
            ("district", QLineEdit),
            ("province", QLineEdit),
            ("department", QLineEdit),
            ("license", QLineEdit),
            ("resolution", QLineEdit),
            ("expiration_date", QDateEdit),
            ("cutoff_date", QDateEdit),
            ("enabled", QComboBox),
        ]
        for key, widget_cls in fields:
            row = QHBoxLayout()
            label = QLabel(translation_service.tr(f"db_table_header_{key}"))
            row.addWidget(label)
            if widget_cls == QLineEdit:
                widget = QLineEdit()
                # Forzar mayúsculas en tiempo real
                widget.textChanged.connect(
                    lambda text, w=widget: (
                        w.setText(text.upper()) if text != text.upper() else None
                    )
                )
                # Autocompletar país en tiempo real si es el campo 'callsign'
                if key == "callsign":
                    widget.textChanged.connect(self._autocomplete_country_from_callsign)
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
        # --- Campo country como combo y campo adicional ---
        row_country = QHBoxLayout()
        label_country = QLabel(translation_service.tr("db_table_header_country"))
        row_country.addWidget(label_country)
        self.country_combo = QComboBox()
        self.country_combo.addItems(["PERU", "OTROS"])
        row_country.addWidget(self.country_combo)
        self.country_other = QLineEdit()
        self.country_other.setPlaceholderText(
            translation_service.tr("other_country_placeholder")
        )
        self.country_other.setEnabled(True)
        self.country_other.textChanged.connect(
            lambda text: (
                self.country_other.setText(text.upper())
                if text != text.upper()
                else None
            )
        )
        row_country.addWidget(self.country_other)
        layout.addLayout(row_country)
        self.inputs["country"] = self.country_combo
        self.inputs["country_other"] = self.country_other
        self.country_combo.currentIndexChanged.connect(self._on_country_changed)
        # Botones
        btns = QHBoxLayout()
        self.btn_ok = QPushButton(translation_service.tr("yes_button"))
        self.btn_cancel = QPushButton(translation_service.tr("no_button"))
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        # Estado inicial: país OTROS
        if not self.operator:
            self.country_combo.setCurrentText("OTROS")
            self.inputs["enabled"].setCurrentIndex(0)  # SI/YES por defecto
            self._on_country_changed(self.country_combo.currentIndex())

    def _on_country_changed(self, idx):
        """
        Habilita o deshabilita campos según el país seleccionado.
        Si es Perú, habilita todos los campos; si es OTROS, deshabilita y limpia los campos específicos de Perú.
        """
        is_peru = self.country_combo.currentText() == "PERU"
        for key in self._peru_fields:
            widget = self.inputs[key]
            if key in ("category", "type"):
                if is_peru:
                    widget.setEnabled(True)
                else:
                    widget.setCurrentText("NO_APLICA")
                    widget.setEnabled(False)
            elif key == "enabled":
                if is_peru:
                    widget.setEnabled(True)
                else:
                    widget.setCurrentIndex(0)  # SI/YES
                    widget.setEnabled(False)
            else:
                widget.setEnabled(is_peru)
                if not is_peru:
                    if isinstance(widget, QLineEdit):
                        widget.clear()
                    elif isinstance(widget, QDateEdit):
                        widget.setDate(QDate.currentDate())
        self.country_other.setEnabled(not is_peru)
        if is_peru:
            self.country_other.clear()

    def _load_operator(self, op):
        """
        Carga los datos de un operador existente en el formulario.
        Args:
            op (obj): Operador a cargar.
        """
        self.inputs["callsign"].setText(getattr(op, "callsign", "").upper())
        self.inputs["name"].setText(getattr(op, "name", "").upper())
        cat = getattr(op, "category", "NOVICIO")
        idx = self.inputs["category"].findText(cat)
        self.inputs["category"].setCurrentIndex(idx if idx >= 0 else 0)
        # type como combo
        type_val = getattr(op, "type_", "OPERADOR")
        idx_type = self.inputs["type"].findText(type_val)
        self.inputs["type"].setCurrentIndex(idx_type if idx_type >= 0 else 0)
        self.inputs["region"].setText(
            getattr(op, "region", "").upper()
        )  # Cargar región
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
        # --- country ---
        country_val = getattr(op, "country", "PERU").upper()
        if country_val == "PERU":
            self.country_combo.setCurrentText("PERU")
            self.country_other.setEnabled(False)
            self.country_other.clear()
        else:
            self.country_combo.setCurrentText("OTROS")
            self.country_other.setEnabled(True)
            self.country_other.setText(country_val)
        self._on_country_changed(self.country_combo.currentIndex())

    def get_operator_data(self):
        """
        Devuelve un dict con los datos ingresados/validados del operador.
        Returns:
            dict: Datos del operador.
        """
        data = {}
        for key, widget in self.inputs.items():
            if key == "country":
                if self.country_combo.currentText() == "PERU":
                    data["country"] = "PERU"
                else:
                    data["country"] = self.country_other.text().strip().upper()
            elif key == "country_other":
                continue
            elif isinstance(widget, QLineEdit):
                data[key] = widget.text().strip().upper()
            elif isinstance(widget, QComboBox):
                if key == "enabled":
                    data[key] = 1 if widget.currentIndex() == 0 else 0
                else:
                    data[key] = widget.currentText()
            elif isinstance(widget, QDateEdit):
                data[key] = widget.date().toString("dd/MM/yyyy")
        # Campo actualizado
        data["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data

    def accept(self):
        """
        Valida los campos obligatorios y formato antes de aceptar el diálogo.
        Si la validación es exitosa, guarda los datos y cierra el diálogo.
        """
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

    def _autocomplete_country_from_callsign(self, text):
        """
        Autocompleta el país en base al indicativo digitado usando callsign_utils y el idioma actual.
        """
        from domain.callsign_utils import callsign_to_country, get_country_full_name
        from translation.translation_service import translation_service

        itu_code = callsign_to_country(text)
        # Obtener idioma actual ('es' o 'en')
        lang_enum = translation_service.get_language()
        lang = (
            getattr(lang_enum, "value", "es")
            if hasattr(lang_enum, "value")
            else str(lang_enum)
        )
        if itu_code:
            country_name = get_country_full_name(itu_code, lang=lang)
            if country_name:
                self.country_combo.setCurrentText("OTROS")
                self.country_other.setText(country_name)
            else:
                self.country_other.clear()
        else:
            self.country_other.clear()
