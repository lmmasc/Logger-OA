"""
ContactEditDialog
Diálogo para editar un contacto del log, con campos y selectores según tipo de log.
Respeta traducción y tipos de datos.
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
    QTimeEdit,
)
from PySide6.QtCore import QDateTime, Qt, QLocale, QTime
from PySide6.QtGui import QIntValidator

# --- Imports de la aplicación ---
from translation.translation_service import translation_service
from config.settings_service import LanguageValue
from interface_adapters.ui.view_manager import LogType
import datetime


class ContactEditDialog(QDialog):
    """
    Diálogo para editar un contacto del log, con campos y selectores según tipo de log.
    Respeta traducción y tipos de datos.
    """

    def __init__(self, contact, log_type, parent=None):
        """
        Inicializa el diálogo de edición de contacto.
        Args:
            contact (dict): Datos del contacto a editar.
            log_type (str): Tipo de log ('ops' o 'contest').
            parent (QWidget, opcional): Widget padre.
        """
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("edit_contact_dialog_title"))
        self.setMinimumWidth(420)
        self.result_contact = None
        self.contact = contact.copy()
        self.log_type = log_type
        layout = QVBoxLayout(self)
        self.inputs = {}
        # Campos comunes
        self.inputs["callsign"] = QLineEdit(self)
        self.inputs["callsign"].setText(contact.get("callsign", ""))
        layout.addWidget(QLabel(translation_service.tr("ui_callsign_label")))
        layout.addWidget(self.inputs["callsign"])
        if self.log_type == LogType.OPERATION_LOG:
            self.inputs["name"] = QLineEdit(self)
            self.inputs["name"].setText(contact.get("name", ""))
            layout.addWidget(QLabel(translation_service.tr("ui_name_label")))
            layout.addWidget(self.inputs["name"])
            self.inputs["country"] = QLineEdit(self)
            self.inputs["country"].setText(contact.get("country", ""))
            layout.addWidget(QLabel(translation_service.tr("ui_country_label")))
            layout.addWidget(self.inputs["country"])
            self.inputs["region"] = QLineEdit(self)
            self.inputs["region"].setText(contact.get("region", ""))
            layout.addWidget(QLabel(translation_service.tr("region")))
            layout.addWidget(self.inputs["region"])
            self.inputs["station"] = QComboBox(self)
            station_keys = [
                "no_data",
                "station_base",
                "station_mobile",
                "station_portable",
            ]
            self.inputs["station"].addItems(
                [translation_service.tr(k) for k in station_keys]
            )
            idx = (
                station_keys.index(contact.get("station", "no_data"))
                if contact.get("station", "no_data") in station_keys
                else 0
            )
            self.inputs["station"].setCurrentIndex(idx)
            layout.addWidget(QLabel(translation_service.tr("station")))
            layout.addWidget(self.inputs["station"])
            self.inputs["energy"] = QComboBox(self)
            energy_keys = [
                "no_data",
                "energy_autonomous",
                "energy_battery",
                "energy_commercial",
            ]
            self.inputs["energy"].addItems(
                [translation_service.tr(k) for k in energy_keys]
            )
            idx = (
                energy_keys.index(contact.get("energy", "no_data"))
                if contact.get("energy", "no_data") in energy_keys
                else 0
            )
            self.inputs["energy"].setCurrentIndex(idx)
            layout.addWidget(QLabel(translation_service.tr("energy")))
            layout.addWidget(self.inputs["energy"])
            self.inputs["power"] = QLineEdit(self)
            self.inputs["power"].setText(str(contact.get("power", "")))
            # Potencia: solo números 1..9999
            self.inputs["power"].setValidator(QIntValidator(1, 9999, self))
            self.inputs["power"].textChanged.connect(
                lambda _: self._validate_field("power")
            )
            layout.addWidget(QLabel(translation_service.tr("power") + " (W)"))
            layout.addWidget(self.inputs["power"])
            self.inputs["rs_rx"] = QLineEdit(self)
            self.inputs["rs_rx"].setText(str(contact.get("rs_rx", "")))
            # RS (RX): solo números de 2 dígitos 11..59
            self.inputs["rs_rx"].setValidator(QIntValidator(11, 59, self))
            self.inputs["rs_rx"].textChanged.connect(
                lambda _: self._validate_field("rs_rx")
            )
            layout.addWidget(QLabel(translation_service.tr("rs_rx")))
            layout.addWidget(self.inputs["rs_rx"])
            self.inputs["rs_tx"] = QLineEdit(self)
            self.inputs["rs_tx"].setText(str(contact.get("rs_tx", "")))
            # RS (TX): solo números de 2 dígitos 11..59
            self.inputs["rs_tx"].setValidator(QIntValidator(11, 59, self))
            self.inputs["rs_tx"].textChanged.connect(
                lambda _: self._validate_field("rs_tx")
            )
            layout.addWidget(QLabel(translation_service.tr("rs_tx")))
            layout.addWidget(self.inputs["rs_tx"])
            self.inputs["obs"] = QLineEdit(self)
            self.inputs["obs"].setText(contact.get("obs", ""))
            layout.addWidget(QLabel(translation_service.tr("observations")))
            layout.addWidget(self.inputs["obs"])
        else:
            # Orden: indicativo, RS_RX, intercambio recibido, RS_TX, intercambio enviado
            self.inputs["rs_rx"] = QLineEdit(self)
            self.inputs["rs_rx"].setText(str(contact.get("rs_rx", "")))
            # RS (RX): solo números de 2 dígitos 11..59
            self.inputs["rs_rx"].setValidator(QIntValidator(11, 59, self))
            self.inputs["rs_rx"].textChanged.connect(
                lambda _: self._validate_field("rs_rx")
            )
            layout.addWidget(QLabel(translation_service.tr("rs_rx")))
            layout.addWidget(self.inputs["rs_rx"])
            self.inputs["exchange_received"] = QLineEdit(self)
            self.inputs["exchange_received"].setText(
                contact.get("exchange_received", "")
            )
            # Intercambio recibido: solo números 1..999
            self.inputs["exchange_received"].setValidator(QIntValidator(1, 999, self))
            self.inputs["exchange_received"].textChanged.connect(
                lambda _: self._validate_field("exchange_received")
            )
            layout.addWidget(QLabel(translation_service.tr("exchange_received")))
            layout.addWidget(self.inputs["exchange_received"])
            self.inputs["rs_tx"] = QLineEdit(self)
            self.inputs["rs_tx"].setText(str(contact.get("rs_tx", "")))
            # RS (TX): solo números de 2 dígitos 11..59
            self.inputs["rs_tx"].setValidator(QIntValidator(11, 59, self))
            self.inputs["rs_tx"].textChanged.connect(
                lambda _: self._validate_field("rs_tx")
            )
            layout.addWidget(QLabel(translation_service.tr("rs_tx")))
            layout.addWidget(self.inputs["rs_tx"])
            self.inputs["exchange_sent"] = QLineEdit(self)
            self.inputs["exchange_sent"].setText(contact.get("exchange_sent", ""))
            # Intercambio enviado: solo números 1..999
            self.inputs["exchange_sent"].setValidator(QIntValidator(1, 999, self))
            self.inputs["exchange_sent"].textChanged.connect(
                lambda _: self._validate_field("exchange_sent")
            )
            layout.addWidget(QLabel(translation_service.tr("exchange_sent")))
            layout.addWidget(self.inputs["exchange_sent"])
            # Agregar campo de observaciones para concursos
            self.inputs["obs"] = QLineEdit(self)
            self.inputs["obs"].setText(contact.get("obs", ""))
            layout.addWidget(QLabel(translation_service.tr("observations")))
            layout.addWidget(self.inputs["obs"])
        # Campo de edición de fecha/hora OA para concursos, UTC para operativos
        ts = contact.get("timestamp", None)
        lang = translation_service.get_language()
        # Detectar locale para abreviatura de mes
        import locale

        try:
            if lang == LanguageValue.ES:
                locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
            else:
                locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
        except locale.Error:
            locale.setlocale(locale.LC_TIME, "C")
        # Guardamos la fecha base (UTC u OA) y mostramos sólo la hora
        time_fmt = "HH:mm"
        if self.log_type == LogType.CONTEST_LOG:
            # Mostrar hora OA (UTC-5)
            if ts:
                dt_utc = datetime.datetime.fromtimestamp(
                    int(ts), tz=datetime.timezone.utc
                )
                dt_oa = dt_utc - datetime.timedelta(hours=5)
                # Guardar fecha OA base para conservarla al aceptar
                self._date_oa = dt_oa.date()
                qt_time = QTime(dt_oa.hour, dt_oa.minute, dt_oa.second)
            else:
                now_utc = datetime.datetime.now(datetime.timezone.utc)
                dt_oa = now_utc - datetime.timedelta(hours=5)
                self._date_oa = dt_oa.date()
                qt_time = QTime(dt_oa.hour, dt_oa.minute, dt_oa.second)
            label = translation_service.tr("edit_contact_datetime_oa")
            self.inputs["time_oa"] = QTimeEdit(qt_time, self)
            self.inputs["time_oa"].setDisplayFormat(time_fmt)
            self.inputs["time_oa"].setTimeSpec(Qt.TimeSpec.LocalTime)
            # Ajustar locale Qt para el widget
            if lang == LanguageValue.ES:
                self.inputs["time_oa"].setLocale(QLocale(QLocale.Language.Spanish))
            else:
                self.inputs["time_oa"].setLocale(QLocale(QLocale.Language.English))
            layout.addWidget(QLabel(label))
            layout.addWidget(self.inputs["time_oa"])
        else:
            # Operativos: mantener UTC
            if ts:
                py_dt_utc = datetime.datetime.fromtimestamp(
                    int(ts), tz=datetime.timezone.utc
                )
            else:
                py_dt_utc = datetime.datetime.now(datetime.timezone.utc)
            label = translation_service.tr("edit_contact_datetime_utc")
            # Guardar fecha UTC base para conservarla al aceptar
            self._date_utc = py_dt_utc.date()
            qt_time = QTime(py_dt_utc.hour, py_dt_utc.minute, py_dt_utc.second)
            self.inputs["time_utc"] = QTimeEdit(qt_time, self)
            self.inputs["time_utc"].setDisplayFormat(time_fmt)
            self.inputs["time_utc"].setTimeSpec(Qt.TimeSpec.UTC)
            # Ajustar locale Qt para el widget
            if lang == LanguageValue.ES:
                self.inputs["time_utc"].setLocale(QLocale(QLocale.Language.Spanish))
            else:
                self.inputs["time_utc"].setLocale(QLocale(QLocale.Language.English))
            layout.addWidget(QLabel(label))
            layout.addWidget(self.inputs["time_utc"])
        # Botones
        btns = QHBoxLayout()
        btn_ok = QPushButton(translation_service.tr("accept_button"), self)
        btn_cancel = QPushButton(translation_service.tr("cancel_button"), self)
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)
        self.setLayout(layout)

        # Validación inicial (marcar inválidos que estén vacíos o fuera de rango)
        for key in ("power", "rs_rx", "rs_tx", "exchange_received", "exchange_sent"):
            if key in self.inputs:
                self._validate_field(key)

    def _validate_field(self, key: str):
        widget = self.inputs.get(key)
        if not isinstance(widget, QLineEdit):
            return
        validator = widget.validator()
        text = widget.text().strip()
        invalid = False
        if isinstance(validator, QIntValidator):
            if text == "":
                invalid = True
            else:
                try:
                    value = int(text)
                    bottom = validator.bottom()
                    top = validator.top()
                    invalid = not (bottom <= value <= top)
                except ValueError:
                    invalid = True
        else:
            invalid = text == ""
        widget.setProperty("invalid", invalid)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def accept(self):
        """
        Obtiene los datos editados del contacto y los guarda en result_contact.
        """
        # Validación final: si algún campo marcado como inválido existe, no cerrar
        invalid_keys = []
        for key in ("power", "rs_rx", "rs_tx", "exchange_received", "exchange_sent"):
            if key in self.inputs:
                self._validate_field(key)
                if self.inputs[key].property("invalid") is True:
                    invalid_keys.append(key)
        if invalid_keys:
            # Mostrar un mensaje simple usando título del diálogo
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self,
                self.windowTitle(),
                translation_service.tr("contact_missing_fields"),
            )
            return
        result = self.contact.copy()
        for k, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                result[k] = widget.text().strip()
            elif isinstance(widget, QComboBox):
                if k == "station":
                    keys = [
                        "no_data",
                        "station_base",
                        "station_mobile",
                        "station_portable",
                    ]
                    result[k] = keys[widget.currentIndex()]
                elif k == "energy":
                    keys = [
                        "no_data",
                        "energy_autonomous",
                        "energy_battery",
                        "energy_commercial",
                    ]
                    result[k] = keys[widget.currentIndex()]
            elif (
                k == "time_oa"
                and self.log_type == LogType.CONTEST_LOG
                and isinstance(widget, QTimeEdit)
            ):
                # Combinar la fecha OA base con la hora editada y convertir a UTC
                qtime = widget.time()
                base_date = getattr(self, "_date_oa", None)
                if base_date is None:
                    # Fallback: hoy en OA
                    now_utc = datetime.datetime.now(datetime.timezone.utc)
                    base_date = (now_utc - datetime.timedelta(hours=5)).date()
                dt_oa_dt = datetime.datetime(
                    base_date.year,
                    base_date.month,
                    base_date.day,
                    qtime.hour(),
                    qtime.minute(),
                    qtime.second(),
                )
                dt_utc = dt_oa_dt + datetime.timedelta(hours=5)
                ts = int(dt_utc.replace(tzinfo=datetime.timezone.utc).timestamp())
                result["timestamp"] = ts
            elif (
                k == "time_utc"
                and self.log_type == LogType.OPERATION_LOG
                and isinstance(widget, QTimeEdit)
            ):
                # Combinar la fecha UTC base con la hora editada
                qtime = widget.time()
                base_date = getattr(self, "_date_utc", None)
                if base_date is None:
                    base_date = datetime.datetime.now(datetime.timezone.utc).date()
                dt_utc_dt = datetime.datetime(
                    base_date.year,
                    base_date.month,
                    base_date.day,
                    qtime.hour(),
                    qtime.minute(),
                    qtime.second(),
                    tzinfo=datetime.timezone.utc,
                )
                ts = int(dt_utc_dt.timestamp())
                result["timestamp"] = ts
        self.result_contact = result
        super().accept()
