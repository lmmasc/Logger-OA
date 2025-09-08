from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QMessageBox,
)
from translation.translation_service import translation_service


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log. Reutilizable en operativos y concursos.
    """

    def __init__(self, parent=None, log_type="ops"):
        super().__init__(parent)
        from .callsign_input_widget import CallsignInputWidget
        from PySide6.QtWidgets import QPushButton, QMessageBox

        self.log_type = log_type
        self.layout = QFormLayout(self)
        # Campo universal: Indicativo (ahora widget independiente)
        self.callsign_input = CallsignInputWidget(self)
        self.layout.addRow(self.callsign_input)
        # Mostrar sugerencias por defecto al iniciar el formulario, pero vacías
        self.callsign_input.set_summary("", show_suggestions=True)
        self.callsign_input.suggestion_list.clear()
        # Campos específicos según tipo de log (orden para operativos)
        if log_type == "ops":
            self.station_input = QLineEdit(self)
            self.layout.addRow(
                QLabel(translation_service.tr("station")), self.station_input
            )
            self.power_input = QLineEdit(self)
            self.layout.addRow(
                QLabel(translation_service.tr("power")), self.power_input
            )
        # Campo universal: Reporte RX
        self.rs_rx_input = QLineEdit(self)
        self.layout.addRow(QLabel(translation_service.tr("rs_rx")), self.rs_rx_input)
        # Campo universal: Reporte TX
        self.rs_tx_input = QLineEdit(self)
        self.layout.addRow(QLabel(translation_service.tr("rs_tx")), self.rs_tx_input)
        # Campo de observaciones
        self.observations_input = QLineEdit(self)
        self.layout.addRow(
            QLabel(translation_service.tr("observations")), self.observations_input
        )
        # Campos específicos para concursos
        if log_type == "contest":
            self.exchange_received_input = QLineEdit(self)
            self.layout.addRow(
                QLabel(translation_service.tr("exchange_received")),
                self.exchange_received_input,
            )
            self.exchange_sent_input = QLineEdit(self)
            self.layout.addRow(
                QLabel(translation_service.tr("exchange_sent")),
                self.exchange_sent_input,
            )

        # Botón para agregar contacto
        self.add_contact_btn = QPushButton(translation_service.tr("add_contact"), self)
        self.layout.addRow(self.add_contact_btn)
        self.add_contact_btn.clicked.connect(self._on_add_contact)

        self.callsign_input.input.textChanged.connect(self._update_callsign_summary)

    def _on_add_contact(self):
        # Recoge datos y llama al caso de uso
        data = self.get_data()
        main_window = self._find_main_window()
        if (
            not main_window
            or not hasattr(main_window, "current_log")
            or not main_window.current_log
        ):
            QMessageBox.warning(
                self,
                translation_service.tr("main_window_title"),
                translation_service.tr("no_log_open"),
            )
            return
        db_path = getattr(main_window.current_log, "db_path", None)
        log_id = getattr(main_window.current_log, "id", None)
        contact_type = "operativo" if self.log_type == "ops" else "concurso"
        try:
            from application.use_cases.contact_management import add_contact_to_log
            from domain.repositories.contact_log_repository import ContactLogRepository

            contact = add_contact_to_log(db_path, log_id, data, contact_type)
            # Recuperar la lista actualizada desde el repositorio
            repo = ContactLogRepository(db_path)
            contacts = repo.get_contacts(log_id)
            main_window.current_log.contacts = contacts
            # Actualiza la tabla en la instancia visible del ViewManager
            if hasattr(main_window, "view_manager"):
                if (
                    self.log_type == "ops"
                    and "log_ops" in main_window.view_manager.views
                ):
                    main_window.view_manager.views["log_ops"].table_widget.set_contacts(
                        contacts
                    )
                elif (
                    self.log_type == "contest"
                    and "log_contest" in main_window.view_manager.views
                ):
                    main_window.view_manager.views[
                        "log_contest"
                    ].table_widget.set_contacts(contacts)
            QMessageBox.information(
                self,
                translation_service.tr("main_window_title"),
                translation_service.tr("contact_added"),
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                translation_service.tr("main_window_title"),
                f"{translation_service.tr('contact_add_failed')}: {e}",
            )

    def _find_main_window(self):
        # Busca la instancia de MainWindow en la jerarquía de padres
        parent = self.parent()
        while parent:
            if parent.__class__.__name__ == "MainWindow":
                return parent
            parent = parent.parent()
        return None

    def get_data(self):
        """Devuelve los datos del formulario como dict."""
        data = {
            "callsign": self.callsign_input.get_callsign(),
            "rs_rx": self.rs_rx_input.text(),
            "rs_tx": self.rs_tx_input.text(),
        }
        if self.log_type == "contest":
            data["exchange_received"] = self.exchange_received_input.text()
            data["exchange_sent"] = self.exchange_sent_input.text()
            data["observations"] = self.observations_input.text()
        elif self.log_type == "ops":
            data["station"] = self.station_input.text()
            data["power"] = self.power_input.text()
            data["obs"] = self.observations_input.text()
        return data

    def retranslate_ui(self):
        """Actualiza los textos según el idioma."""
        self.callsign_input.retranslate_ui()
        self.layout.labelForField(self.rs_rx_input).setText(
            translation_service.tr("rs_rx")
        )
        self.layout.labelForField(self.rs_tx_input).setText(
            translation_service.tr("rs_tx")
        )
        self.layout.labelForField(self.observations_input).setText(
            translation_service.tr("observations")
        )
        if self.log_type == "contest":
            self.layout.labelForField(self.exchange_received_input).setText(
                translation_service.tr("exchange_received")
            )
            self.layout.labelForField(self.exchange_sent_input).setText(
                translation_service.tr("exchange_sent")
            )
        elif self.log_type == "ops":
            self.layout.labelForField(self.station_input).setText(
                translation_service.tr("station")
            )
            self.layout.labelForField(self.power_input).setText(
                translation_service.tr("power")
            )

    def _update_callsign_summary(self):
        callsign = self.callsign_input.get_callsign().strip().upper()
        summary = ""
        if callsign:
            from infrastructure.repositories.sqlite_radio_operator_repository import (
                SqliteRadioOperatorRepository,
            )

            repo = SqliteRadioOperatorRepository()
            operator = (
                repo.get_operator_by_callsign(callsign)
                if hasattr(repo, "get_operator_by_callsign")
                else None
            )
            if operator:
                # Formato en tabla 3x3
                enabled = (
                    translation_service.tr("enabled")
                    if operator.enabled
                    else translation_service.tr("disabled")
                )
                summary = f"<table width='100%' style='font-size:16px;'>"
                summary += "<tr>"
                summary += f"<td><b>{operator.name}</b></td>"
                summary += f"<td>{translation_service.tr('district')}: {operator.district}</td>"
                summary += f"<td>{translation_service.tr('category')}: {operator.category}</td>"
                summary += "</tr><tr>"
                summary += (
                    f"<td>{translation_service.tr('country')}: {operator.country}</td>"
                )
                summary += f"<td>{translation_service.tr('province')}: {operator.province}</td>"
                summary += (
                    f"<td>{translation_service.tr('type')}: {operator.type_}</td>"
                )
                summary += "</tr><tr>"
                summary += f"<td>{translation_service.tr('enabled') if operator.enabled else translation_service.tr('disabled')}</td>"
                summary += f"<td>{translation_service.tr('department')}: {operator.department}</td>"
                summary += f"<td>{translation_service.tr('expiration')}: {operator.expiration_date}</td>"
                summary += "</tr></table>"
                self.callsign_input.set_summary(summary, show_suggestions=False)
            else:
                # Si no hay coincidencia, mostrar lista de sugerencias
                self.callsign_input.set_summary("", show_suggestions=True)
        else:
            self.callsign_input.set_summary("", show_suggestions=True)
