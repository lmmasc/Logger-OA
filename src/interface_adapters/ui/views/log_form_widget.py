from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)
from translation.translation_service import translation_service
from PySide6.QtCore import Qt


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log. Reutilizable en operativos y concursos.
    """

    def __init__(
        self,
        parent=None,
        log_type="ops",
        callsign="",
        log_type_name="",
        log_date="",
    ):
        super().__init__(parent)

        self.log_type = log_type
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # --- Formulario horizontal ---
        form_row = QHBoxLayout()
        form_row.setSpacing(4)
        form_row.setContentsMargins(0, 0, 0, 0)

        # Station
        self.station_input = QComboBox(self)
        self.station_input.addItems(
            [
                translation_service.tr("no_data"),
                translation_service.tr("station_base"),
                translation_service.tr("station_mobile"),
                translation_service.tr("station_portable"),
            ]
        )
        self.station_input.setCurrentIndex(0)
        self.station_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        station_label = QLabel(translation_service.tr("station"))
        station_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        station_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_row.addWidget(station_label)
        form_row.addWidget(self.station_input)
        self.station_label = station_label

        # Energy
        self.energy_input = QComboBox(self)
        self.energy_input.addItems(
            [
                translation_service.tr("no_data"),
                translation_service.tr("energy_autonomous"),
                translation_service.tr("energy_battery"),
                translation_service.tr("energy_commercial"),
            ]
        )
        self.energy_input.setCurrentIndex(0)
        self.energy_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        energy_label = QLabel(translation_service.tr("energy"))
        energy_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        energy_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_row.addWidget(energy_label)
        form_row.addWidget(self.energy_input)
        self.energy_label = energy_label

        # Power
        self.power_input = QLineEdit(self)
        self.power_input.setText("1")
        self.power_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        power_label = QLabel(translation_service.tr("power"))
        power_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        power_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_row.addWidget(power_label)
        form_row.addWidget(self.power_input)
        self.power_label = power_label

        # RS_RX
        self.rs_rx_input = QLineEdit(self)
        self.rs_rx_input.setText("59")
        self.rs_rx_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        rs_rx_label = QLabel(translation_service.tr("rs_rx"))
        rs_rx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        rs_rx_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_row.addWidget(rs_rx_label)
        form_row.addWidget(self.rs_rx_input)
        self.rs_rx_label = rs_rx_label

        # RS_TX
        self.rs_tx_input = QLineEdit(self)
        self.rs_tx_input.setText("59")
        self.rs_tx_input.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        rs_tx_label = QLabel(translation_service.tr("rs_tx"))
        rs_tx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        rs_tx_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_row.addWidget(rs_tx_label)
        form_row.addWidget(self.rs_tx_input)
        self.rs_tx_label = rs_tx_label

        # Observaciones (expansivo)
        self.observations_input = QLineEdit(self)
        self.observations_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        obs_label = QLabel(translation_service.tr("observations"))
        obs_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        obs_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_row.addWidget(obs_label)
        form_row.addWidget(self.observations_input)
        self.observations_label = obs_label

        # Widget del formulario
        form_row_widget = QWidget(self)
        form_row_widget.setLayout(form_row)
        form_row_widget.setMinimumWidth(700)
        form_row_widget.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )  # No expansivo, solo lo necesario
        main_layout.addWidget(form_row_widget)

        # Asignar layout principal
        self.setLayout(main_layout)

    def _on_add_contact(self, callsign=None):
        # Recoge datos y llama al caso de uso
        data = self.get_data(callsign)
        if callsign:
            data["callsign"] = callsign
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

    def get_data(self, callsign=None):
        """Devuelve los datos del formulario como dict."""
        data = {
            "callsign": callsign if callsign is not None else "",
            "rs_rx": self.rs_rx_input.text(),
            "rs_tx": self.rs_tx_input.text(),
        }
        if self.log_type == "contest":
            data["exchange_received"] = self.exchange_received_input.text()
            data["exchange_sent"] = self.exchange_sent_input.text()
            data["observations"] = self.observations_input.text()
        elif self.log_type == "ops":
            data["station"] = (
                self.station_input.currentText() if self.station_input else ""
            )
            data["energy"] = (
                self.energy_input.currentText() if self.energy_input else ""
            )
            data["power"] = self.power_input.text()
            data["obs"] = self.observations_input.text()
        return data

    def retranslate_ui(self):
        """Actualiza los textos según el idioma."""
        # Actualizar todos los labels manualmente por el nuevo layout
        if hasattr(self, "station_label"):
            self.station_label.setText(translation_service.tr("station"))
        if hasattr(self, "energy_label"):
            self.energy_label.setText(translation_service.tr("energy"))
        if hasattr(self, "power_label"):
            self.power_label.setText(translation_service.tr("power"))
        if hasattr(self, "rs_rx_label"):
            self.rs_rx_label.setText(translation_service.tr("rs_rx"))
        if hasattr(self, "rs_tx_label"):
            self.rs_tx_label.setText(translation_service.tr("rs_tx"))
        if hasattr(self, "observations_label"):
            self.observations_label.setText(translation_service.tr("observations"))
        if hasattr(self, "exchange_received_label"):
            self.exchange_received_label.setText(
                translation_service.tr("exchange_received")
            )
        if hasattr(self, "exchange_sent_label"):
            self.exchange_sent_label.setText(translation_service.tr("exchange_sent"))
        # Traducir opciones de los selectores
        if hasattr(self, "station_input") and isinstance(self.station_input, QComboBox):
            items = [
                translation_service.tr("no_data"),
                translation_service.tr("station_base"),
                translation_service.tr("station_mobile"),
                translation_service.tr("station_portable"),
            ]
            current = self.station_input.currentIndex()
            self.station_input.clear()
            self.station_input.addItems(items)
            self.station_input.setCurrentIndex(current)
        if hasattr(self, "energy_input") and isinstance(self.energy_input, QComboBox):
            items = [
                translation_service.tr("no_data"),
                translation_service.tr("energy_autonomous"),
                translation_service.tr("energy_battery"),
                translation_service.tr("energy_commercial"),
            ]
            current = self.energy_input.currentIndex()
            self.energy_input.clear()
            self.energy_input.addItems(items)
            self.energy_input.setCurrentIndex(current)
        # Eliminar traducción de labels de relojes, ya que ahora se gestionan en las vistas
