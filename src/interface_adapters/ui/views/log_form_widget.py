from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox
from translation.translation_service import translation_service


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log. Reutilizable en operativos y concursos.
    """

    def __init__(self, parent=None, log_type="ops"):
        super().__init__(parent)
        from .callsign_input_widget import CallsignInputWidget

        self.log_type = log_type
        self.layout = QFormLayout(self)
        # Campo universal: Indicativo (ahora widget independiente)
        self.callsign_input = CallsignInputWidget(self)
        self.layout.addRow(self.callsign_input)
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

    def get_data(self):
        """Devuelve los datos del formulario como dict."""
        data = {
            "callsign": self.callsign_input.get_callsign(),
            "rs_rx": self.rs_rx_input.text(),
            "rs_tx": self.rs_tx_input.text(),
            "observations": self.observations_input.text(),
        }
        if self.log_type == "contest":
            data["exchange_received"] = self.exchange_received_input.text()
            data["exchange_sent"] = self.exchange_sent_input.text()
        elif self.log_type == "ops":
            data["station"] = self.station_input.text()
            data["power"] = self.power_input.text()
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
