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
from datetime import timezone, timedelta


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
            "department",
            "province",
            "district",
            "license",
            "resolution",
            "expiration_date",
            "cutoff_date",
            "enabled",
        ]
        # Campos básicos (sin country)
        # Inicializar widgets de categoría
        category_row = QHBoxLayout()
        category_label = QLabel(translation_service.tr("db_table_header_category"))
        category_row.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["NOVICIO", "INTERMEDIO", "SUPERIOR"])
        self.category_line = QLineEdit()
        self.category_line.textChanged.connect(
            lambda text, w=self.category_line: (
                w.setText(text.upper()) if text != text.upper() else None
            )
        )
        category_row.addWidget(self.category_combo)
        category_row.addWidget(self.category_line)
        self.category_line.hide()
        self.inputs["category_combo"] = self.category_combo
        self.inputs["category_line"] = self.category_line
        self.inputs["category"] = self.category_combo

        fields = [
            ("callsign", QLineEdit),
            ("name", QLineEdit),
            ("type", QComboBox),
            ("country", QComboBox),
            ("region", QLineEdit),
            ("department", QLineEdit),
            ("province", QLineEdit),
            ("district", QLineEdit),
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
                widget.textChanged.connect(
                    lambda text, w=widget: (
                        w.setText(text.upper()) if text != text.upper() else None
                    )
                )
                if key == "callsign":
                    widget.textChanged.connect(self._autocomplete_country_from_callsign)
                row.addWidget(widget)
                self.inputs[key] = widget
            elif widget_cls == QComboBox:
                widget = QComboBox()
                if key == "type":
                    widget.addItems(["OPERADOR", "INSTALADOR/OPERADOR", "NO_APLICA"])
                elif key == "enabled":
                    widget.addItems(
                        [translation_service.tr("yes"), translation_service.tr("no")]
                    )
                row.addWidget(widget)
                self.inputs[key] = widget
            elif widget_cls == QDateEdit:
                widget = QDateEdit()
                widget.setDisplayFormat("dd/MM/yyyy")
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
                row.addWidget(widget)
                self.inputs[key] = widget
            # Agregar el row de categoría justo después del nombre
            if key == "name":
                layout.addLayout(row)
                layout.addLayout(category_row)
            else:
                layout.addLayout(row)
        # Inicializar el combo de país después de crearlo en el bucle
        from domain.itu_country_names import ITU_COUNTRY_NAMES
        from utils.text import normalize_ascii

        lang = "es"
        if hasattr(translation_service, "get_language"):
            lang_enum = translation_service.get_language()
            lang = getattr(lang_enum, "value", str(lang_enum))
        country_items = []
        for itu_code, names in ITU_COUNTRY_NAMES.items():
            name = names.get(lang, names.get("es", ""))
            if name:
                country_items.append((itu_code, normalize_ascii(name)))
        country_items.sort(key=lambda x: x[1])
        country_combo = self.inputs["country"]
        for itu_code, name in country_items:
            country_combo.addItem(name, itu_code)
        country_combo.currentIndexChanged.connect(self._on_country_changed)
        # Botones y estado inicial
        btns = QHBoxLayout()
        btn_ok = QPushButton(translation_service.tr("yes_button"))
        btn_cancel = QPushButton(translation_service.tr("no_button"))
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        # Estado inicial: país PER
        if not self.operator:
            idx_peru = self.inputs["country"].findData("PER")
            if idx_peru >= 0:
                self.inputs["country"].setCurrentIndex(idx_peru)
            self.inputs["enabled"].setCurrentIndex(0)  # SI/YES por defecto
            self._on_country_changed(self.inputs["country"].currentIndex())

        if (
            "department" in self.inputs
            and "province" in self.inputs
            and "district" in self.inputs
        ):
            self.inputs["department"].textChanged.connect(self._update_region_peru)
            self.inputs["province"].textChanged.connect(self._update_region_peru)
            self.inputs["district"].textChanged.connect(self._update_region_peru)

    def _update_region_peru(self):
        """
        Actualiza el campo 'region' dinámicamente si país es Perú.
        """
        if self._get_widget_text(self.inputs["country"]) == "PERU":
            departamento = self.inputs["department"].text().strip().upper()
            provincia = self.inputs["province"].text().strip().upper()
            distrito = self.inputs["district"].text().strip().upper()
            region_value = (
                f"{departamento}-{provincia}-{distrito}"
                if departamento or provincia or distrito
                else ""
            )
            self.inputs["region"].setText(region_value)

    def _on_country_changed(self, idx):
        """
        Habilita o deshabilita campos según el país seleccionado.
        Si es Perú, habilita todos los campos; si es OTROS, deshabilita y limpia los campos específicos de Perú.
        """
        is_peru = self._get_widget_text(self.inputs["country"]) == "PERU"
        for key in self._peru_fields:
            if key == "category":
                # Solo cambiar si los widgets existen
                if hasattr(self, "category_combo") and hasattr(self, "category_line"):
                    if is_peru:
                        self.category_combo.show()
                        self.category_line.hide()
                        self.category_combo.setEnabled(True)
                        self.inputs["category"] = self.category_combo
                    else:
                        self.category_combo.hide()
                        self.category_line.show()
                        self.category_line.setEnabled(True)
                        self.inputs["category"] = self.category_line
                continue
            widget = self.inputs[key]
            # Habilitar siempre 'license', 'resolution', 'expiration_date' y 'cutoff_date' para todos los países
            if key in ("license", "resolution", "expiration_date", "cutoff_date"):
                widget.setEnabled(True)
                continue
            if key == "type":
                if is_peru:
                    widget.setEnabled(True)
                else:
                    self._set_widget_text(widget, "NO_APLICA")
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

        # Deshabilitar y autollenar 'region' para Perú
        region_widget = self.inputs["region"]
        if is_peru:
            region_widget.setEnabled(False)
            departamento = self.inputs["department"].text().strip().upper()
            provincia = self.inputs["province"].text().strip().upper()
            distrito = self.inputs["district"].text().strip().upper()
            region_value = (
                f"{departamento}-{provincia}-{distrito}"
                if departamento or provincia or distrito
                else ""
            )
            region_widget.setText(region_value)
        else:
            region_widget.setEnabled(True)
        # country_other eliminado: solo combo ITU

    def _load_operator(self, op):
        """
        Carga los datos de un operador existente en el formulario.
        Args:
            op (obj): Operador a cargar.
        """
        self.inputs["callsign"].setText(getattr(op, "callsign", "").upper())
        self.inputs["name"].setText(getattr(op, "name", "").upper())
        cat = getattr(op, "category", "NOVICIO")
        is_peru = getattr(op, "country", "PER") == "PER"
        if hasattr(self, "category_combo") and hasattr(self, "category_line"):
            if is_peru:
                idx = self.category_combo.findText(cat)
                self.category_combo.setCurrentIndex(idx if idx >= 0 else 0)
                self.category_combo.show()
                self.category_line.hide()
            else:
                self.category_line.setText(cat.upper())
                self.category_line.show()
                self.category_combo.hide()
        # type como combo
        type_val = getattr(op, "type_", "OPERADOR")
        idx_type = self.inputs["type"].findText(type_val)
        self.inputs["type"].setCurrentIndex(idx_type if idx_type >= 0 else 0)
        self.inputs["region"].setText(getattr(op, "region", "").upper())
        self.inputs["district"].setText(getattr(op, "district", "").upper())
        self.inputs["province"].setText(getattr(op, "province", "").upper())
        self.inputs["department"].setText(getattr(op, "department", "").upper())
        # Cargar correctamente 'license' y 'resolution' para cualquier país
        license_val = getattr(op, "license_", getattr(op, "license", ""))
        self.inputs["license"].setText(license_val.upper())
        self.inputs["resolution"].setText(getattr(op, "resolution", "").upper())
        # Fechas
        from datetime import datetime, timezone, timedelta

        for key in ("expiration_date", "cutoff_date"):
            val = getattr(op, key, None)
            if isinstance(val, int) and val > 0:
                try:
                    dt_utc = datetime.fromtimestamp(val, timezone.utc)
                    dt_peru = dt_utc.astimezone(timezone(timedelta(hours=-5)))
                    self.inputs[key].setDate(
                        QDate(dt_peru.year, dt_peru.month, dt_peru.day)
                    )
                except Exception:
                    self.inputs[key].setDate(QDate.currentDate())
            else:
                self.inputs[key].setDate(QDate.currentDate())
        # Seleccionar país en combo por ITU
        itu_code = getattr(op, "country", "PER")
        idx_country = self.inputs["country"].findData(itu_code)
        if idx_country >= 0:
            self.inputs["country"].setCurrentIndex(idx_country)
        self._on_country_changed(self.inputs["country"].currentIndex())

        # Cargar el valor de 'enabled' en el combo
        enabled_val = getattr(op, "enabled", 1)
        self.inputs["enabled"].setCurrentIndex(0 if enabled_val else 1)

    def get_operator_data(self):
        """
        Devuelve un dict con los datos ingresados/validados del operador.
        Returns:
            dict: Datos del operador válidos para RadioOperator.
        """
        data = {}

        # Mapeo de campos UI a campos del modelo
        field_mapping = {
            "callsign": "callsign",
            "name": "name",
            "category": "category",
            "type": "type_",
            "region": "region",
            "district": "district",
            "province": "province",
            "department": "department",
            "license": "license_",
            "resolution": "resolution",
            "expiration_date": "expiration_date",
            "cutoff_date": "cutoff_date",
            "enabled": "enabled",
            "country": "country",
        }

        for ui_key, model_key in field_mapping.items():
            if ui_key not in self.inputs:
                continue

            widget = self.inputs[ui_key]

            if ui_key == "country":
                idx = widget.currentIndex()
                data[model_key] = widget.itemData(idx)
            elif isinstance(widget, QLineEdit):
                data[model_key] = widget.text().strip().upper()
            elif isinstance(widget, QComboBox):
                if ui_key == "enabled":
                    data[model_key] = 1 if widget.currentIndex() == 0 else 0
                else:
                    # Para category, usar el widget correcto (puede ser combo o lineedit)
                    if ui_key == "category":
                        data[model_key] = self._get_widget_text(widget).strip()
                    else:
                        data[model_key] = self._get_widget_text(widget)
            elif isinstance(widget, QDateEdit):
                # Convertir fecha local Perú a timestamp UTC
                qdate = widget.date()
                dt_peru = datetime.datetime(
                    qdate.year(),
                    qdate.month(),
                    qdate.day(),
                    tzinfo=timezone(timedelta(hours=-5)),
                )
                dt_utc = dt_peru.astimezone(timezone.utc)
                data[model_key] = int(dt_utc.timestamp())

        # Campo actualizado: timestamp UTC con fecha y hora
        data["updated_at"] = int(datetime.datetime.now(timezone.utc).timestamp())
        return data

    def _get_widget_text(self, widget):
        """
        Obtiene el texto de un widget, sea QComboBox o QLineEdit.

        Args:
            widget: Widget del que obtener el texto

        Returns:
            str: Texto del widget
        """
        if hasattr(widget, "currentText"):
            return widget.currentText()
        elif hasattr(widget, "text"):
            return widget.text()
        else:
            return str(widget.text()) if hasattr(widget, "text") else ""

    def _set_widget_text(self, widget, text):
        """
        Establece el texto de un widget, sea QComboBox o QLineEdit.

        Args:
            widget: Widget al que establecer el texto
            text: Texto a establecer
        """
        if hasattr(widget, "setCurrentText"):
            widget.setCurrentText(text)
        elif hasattr(widget, "setText"):
            widget.setText(text)

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
        # Validar categoría solo para operadores peruanos
        country_text = self._get_widget_text(self.inputs["country"])
        if country_text == "PERU":
            category_text = self._get_widget_text(self.inputs["category"])
            if category_text not in (
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
        from domain.callsign_utils import callsign_to_country

        itu_code = callsign_to_country(text)
        if itu_code:
            idx = self.inputs["country"].findData(itu_code)
            if idx >= 0:
                self.inputs["country"].setCurrentIndex(idx)
