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
from translation.translation_service import translation_service


class ContactEditDialog(QDialog):
    def accept(self):
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
                and self.log_type == "contest"
                and isinstance(widget, QDateTimeEdit)
            ):
                import datetime
                dt_oa = widget.dateTime().toPython()
                dt_utc = dt_oa + datetime.timedelta(hours=5)
                ts = int(dt_utc.replace(tzinfo=datetime.timezone.utc).timestamp())
                result["timestamp"] = ts
            elif (
                k == "datetime_utc"
                and self.log_type == "ops"
                and isinstance(widget, QDateTimeEdit)
            ):
                ts = widget.dateTime().toSecsSinceEpoch()
                result["timestamp"] = ts
        self.result_contact = result
        super().accept()
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
        # Campo de edición de fecha/hora OA para concursos, UTC para operativos
        ts = contact.get("timestamp", None)
        lang = translation_service.get_language()
        if self.log_type == "contest":
            # Mostrar hora OA (UTC-5)
            if ts:
                import datetime

                dt_utc = datetime.datetime.utcfromtimestamp(int(ts))
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
            if lang == "es":
                date_fmt = "HH:mm dd/MM/yyyy 'OA'"
                label = "Hora OA (UTC-5)"
            else:
                date_fmt = "HH:mm MM/dd/yyyy 'OA'"
                label = "OA Time (UTC-5)"
            self.inputs["datetime_oa"] = QDateTimeEdit(dt_qt, self)
            self.inputs["datetime_oa"].setDisplayFormat(date_fmt)
            self.inputs["datetime_oa"].setTimeSpec(Qt.LocalTime)
            layout.addWidget(QLabel(label))
            layout.addWidget(self.inputs["datetime_oa"])
        else:
            # Operativos: mantener UTC
            if ts:
                dt_utc = QDateTime.fromSecsSinceEpoch(int(ts), Qt.UTC)
            else:
                dt_utc = QDateTime.currentDateTimeUtc()
            if lang == "es":
                date_fmt = "HH:mm dd/MM/yyyy 'UTC'"
                label = translation_service.tr("edit_contact_datetime_utc_es")
            else:
                date_fmt = "HH:mm MM/dd/yyyy 'UTC'"
                label = translation_service.tr("edit_contact_datetime_utc_en")
            self.inputs["datetime_utc"] = QDateTimeEdit(dt_utc, self)
            self.inputs["datetime_utc"].setDisplayFormat(date_fmt)
            self.inputs["datetime_utc"].setTimeSpec(Qt.UTC)
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
        print("[DEBUG] Registro original:", self.contact)
        result = self.contact.copy()
        for k, widget in self.inputs.items():
            print(f"[DEBUG] Procesando campo: {k}, valor antes: {result.get(k)}")
            if isinstance(widget, QLineEdit):
                result[k] = widget.text().strip()
                print(f"[DEBUG] Nuevo valor QLineEdit: {result[k]}")
            elif isinstance(widget, QComboBox):
                if k == "station":
                    keys = [
                        "no_data",
                        "station_base",
                        "station_mobile",
                        "station_portable",
                    ]
                    result[k] = keys[widget.currentIndex()]
                    print(f"[DEBUG] Nuevo valor station: {result[k]}")
                elif k == "energy":
                    keys = [
                        "no_data",
                        "energy_autonomous",
                        "energy_battery",
                        "energy_commercial",
                    ]
                    result[k] = keys[widget.currentIndex()]
                    print(f"[DEBUG] Nuevo valor energy: {result[k]}")
            elif (
                k == "datetime_oa"
                and self.log_type == "contest"
                and isinstance(widget, QDateTimeEdit)
            ):
                import datetime

                dt_oa = widget.dateTime().toPython()
                print(f"[DEBUG] Valor datetime_oa editado: {dt_oa}")
                dt_utc = dt_oa + datetime.timedelta(hours=5)
                ts = int(dt_utc.replace(tzinfo=datetime.timezone.utc).timestamp())
                result["timestamp"] = ts
                print(f"[DEBUG] Nuevo timestamp (contest): {ts}")
            elif (
                k == "datetime_utc"
                and self.log_type == "ops"
                and isinstance(widget, QDateTimeEdit)
            ):
                ts = widget.dateTime().toSecsSinceEpoch()
                result["timestamp"] = ts
                print(f"[DEBUG] Nuevo timestamp (ops): {ts}")
        print("[DEBUG] Registro final para guardar:", result)
        self.result_contact = result
        super().accept()
