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
    QDateTimeEdit,
)
from PySide6.QtCore import QDateTime, Qt

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
            layout.addWidget(QLabel(translation_service.tr("power") + " (W)"))
            layout.addWidget(self.inputs["power"])
            self.inputs["rs_rx"] = QLineEdit(self)
            self.inputs["rs_rx"].setText(str(contact.get("rs_rx", "")))
            layout.addWidget(QLabel(translation_service.tr("rs_rx")))
            layout.addWidget(self.inputs["rs_rx"])
            self.inputs["rs_tx"] = QLineEdit(self)
            self.inputs["rs_tx"].setText(str(contact.get("rs_tx", "")))
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
            layout.addWidget(QLabel(translation_service.tr("rs_rx")))
            layout.addWidget(self.inputs["rs_rx"])
            self.inputs["exchange_received"] = QLineEdit(self)
            self.inputs["exchange_received"].setText(
                contact.get("exchange_received", "")
            )
            layout.addWidget(QLabel(translation_service.tr("exchange_received")))
            layout.addWidget(self.inputs["exchange_received"])
            self.inputs["rs_tx"] = QLineEdit(self)
            self.inputs["rs_tx"].setText(str(contact.get("rs_tx", "")))
            layout.addWidget(QLabel(translation_service.tr("rs_tx")))
            layout.addWidget(self.inputs["rs_tx"])
            self.inputs["exchange_sent"] = QLineEdit(self)
            self.inputs["exchange_sent"].setText(contact.get("exchange_sent", ""))
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
        if self.log_type == LogType.CONTEST_LOG:
            # Mostrar hora OA (UTC-5)
            if ts:
                dt_utc = datetime.datetime.fromtimestamp(
                    int(ts), tz=datetime.timezone.utc
                )
                dt_oa = dt_utc - datetime.timedelta(hours=5)
                dt_qt = QDateTime(
                    dt_oa.year,
                    dt_oa.month,
                    dt_oa.day,
                    dt_oa.hour,
                    dt_oa.minute,
                    dt_oa.second,
                )
            else:
                dt_qt = QDateTime.currentDateTime()
            if lang == LanguageValue.ES:
                date_fmt = "HH:mm dd/MM/yyyy 'OA'"
                label = "Hora OA (UTC-5)"
            else:
                date_fmt = "HH:mm MM/dd/yyyy 'OA'"
                label = "OA Time (UTC-5)"
            self.inputs["datetime_oa"] = QDateTimeEdit(dt_qt, self)
            self.inputs["datetime_oa"].setDisplayFormat(date_fmt)
            self.inputs["datetime_oa"].setTimeSpec(Qt.TimeSpec.LocalTime)
            layout.addWidget(QLabel(label))
            layout.addWidget(self.inputs["datetime_oa"])
        else:
            # Operativos: mantener UTC
            if ts:
                dt_utc = QDateTime.fromSecsSinceEpoch(int(ts), Qt.TimeSpec.UTC)
            else:
                dt_utc = QDateTime.currentDateTimeUtc()
            # El formato de fecha sigue dependiendo del idioma, pero el label se traduce con una sola clave
            if lang == LanguageValue.ES:
                date_fmt = "HH:mm dd/MM/yyyy 'UTC'"
            else:
                date_fmt = "HH:mm MM/dd/yyyy 'UTC'"
            label = translation_service.tr("edit_contact_datetime_utc")
            self.inputs["datetime_utc"] = QDateTimeEdit(dt_utc, self)
            self.inputs["datetime_utc"].setDisplayFormat(date_fmt)
            self.inputs["datetime_utc"].setTimeSpec(Qt.TimeSpec.UTC)
            layout.addWidget(QLabel(label))
            layout.addWidget(self.inputs["datetime_utc"])
        # Botones
        btns = QHBoxLayout()
        btn_ok = QPushButton(translation_service.tr("ok_button"), self)
        btn_cancel = QPushButton(translation_service.tr("cancel_button"), self)
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)
        self.setLayout(layout)

    def accept(self):
        """
        Obtiene los datos editados del contacto y los guarda en result_contact.
        """
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
                k == "datetime_oa"
                and self.log_type == LogType.CONTEST_LOG
                and isinstance(widget, QDateTimeEdit)
            ):
                # Convertir QDateTime a datetime.datetime antes de sumar timedelta
                dt_oa_dt = widget.dateTime().toPython()
                import datetime as dtmod

                if isinstance(dt_oa_dt, dtmod.datetime):
                    dt_utc = dt_oa_dt + dtmod.timedelta(hours=5)
                    ts = int(dt_utc.replace(tzinfo=dtmod.timezone.utc).timestamp())
                    result["timestamp"] = ts
                else:
                    # Si no es datetime, intentar convertir
                    dt_oa_dt = dtmod.datetime.fromisoformat(str(dt_oa_dt))
                    dt_utc = dt_oa_dt + dtmod.timedelta(hours=5)
                    ts = int(dt_utc.replace(tzinfo=dtmod.timezone.utc).timestamp())
                    result["timestamp"] = ts
            elif (
                k == "datetime_utc"
                and self.log_type == LogType.OPERATION_LOG
                and isinstance(widget, QDateTimeEdit)
            ):
                ts = widget.dateTime().toSecsSinceEpoch()
                result["timestamp"] = ts
        self.result_contact = result
        super().accept()
