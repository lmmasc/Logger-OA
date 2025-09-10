from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)
from translation.translation_service import translation_service


class ContactEditDialog(QDialog):
    """
    Diálogo para editar un contacto del log, con campos y selectores según tipo de log.
    Respeta traducción y tipos de datos.
    """

    def __init__(self, contact, log_type, parent=None):
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
        layout.addWidget(QLabel(translation_service.tr("table_header_callsign")))
        layout.addWidget(self.inputs["callsign"])
        if log_type == "ops":
            self.inputs["name"] = QLineEdit(self)
            self.inputs["name"].setText(contact.get("name", ""))
            layout.addWidget(QLabel(translation_service.tr("name")))
            layout.addWidget(self.inputs["name"])
            self.inputs["country"] = QLineEdit(self)
            self.inputs["country"].setText(contact.get("country", ""))
            layout.addWidget(QLabel(translation_service.tr("country")))
            layout.addWidget(self.inputs["country"])
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
        else:
            self.inputs["exchange_received"] = QLineEdit(self)
            self.inputs["exchange_received"].setText(
                contact.get("exchange_received", "")
            )
            layout.addWidget(QLabel(translation_service.tr("exchange_received")))
            layout.addWidget(self.inputs["exchange_received"])
            self.inputs["exchange_sent"] = QLineEdit(self)
            self.inputs["exchange_sent"].setText(contact.get("exchange_sent", ""))
            layout.addWidget(QLabel(translation_service.tr("exchange_sent")))
            layout.addWidget(self.inputs["exchange_sent"])
            self.inputs["rs_rx"] = QLineEdit(self)
            self.inputs["rs_rx"].setText(str(contact.get("rs_rx", "")))
            layout.addWidget(QLabel(translation_service.tr("rs_rx")))
            layout.addWidget(self.inputs["rs_rx"])
            self.inputs["rs_tx"] = QLineEdit(self)
            self.inputs["rs_tx"].setText(str(contact.get("rs_tx", "")))
            layout.addWidget(QLabel(translation_service.tr("rs_tx")))
            layout.addWidget(self.inputs["rs_tx"])
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
        # Validar y construir el resultado
        result = {}
        for k, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                result[k] = widget.text().strip()
            elif isinstance(widget, QComboBox):
                # Guardar la key, no el texto traducido
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
        self.result_contact = result
        super().accept()
