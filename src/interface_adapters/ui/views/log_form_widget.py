from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox
from translation.translation_service import translation_service


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log. Reutilizable en operativos y concursos.
    """

    def __init__(self, parent=None, log_type="ops"):
        super().__init__(parent)
        self.log_type = log_type
        self.layout = QFormLayout(self)
        # Campo universal: Indicativo
        self.callsign_input = QLineEdit(self)
        self.layout.addRow(
            QLabel(translation_service.tr("callsign")), self.callsign_input
        )
        # Campo universal: Hora
        self.time_input = QLineEdit(self)
        self.layout.addRow(QLabel(translation_service.tr("time")), self.time_input)
        # Campo universal: Reporte RX
        self.rs_rx_input = QLineEdit(self)
        self.layout.addRow(QLabel(translation_service.tr("rs_rx")), self.rs_rx_input)
        # Campo universal: Reporte TX
        self.rs_tx_input = QLineEdit(self)
        self.layout.addRow(QLabel(translation_service.tr("rs_tx")), self.rs_tx_input)
        # Campos específicos según tipo de log
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
        elif log_type == "ops":
            self.station_input = QLineEdit(self)
            self.layout.addRow(
                QLabel(translation_service.tr("station")), self.station_input
            )
            self.power_input = QLineEdit(self)
            self.layout.addRow(
                QLabel(translation_service.tr("power")), self.power_input
            )
        # Puedes agregar más campos según necesidades

    def get_data(self):
        """Devuelve los datos del formulario como dict."""
        data = {
            "callsign": self.callsign_input.text(),
            "time": self.time_input.text(),
            "rs_rx": self.rs_rx_input.text(),
            "rs_tx": self.rs_tx_input.text(),
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
        self.layout.labelForField(self.callsign_input).setText(
            translation_service.tr("callsign")
        )
        self.layout.labelForField(self.time_input).setText(
            translation_service.tr("time")
        )
        self.layout.labelForField(self.rs_rx_input).setText(
            translation_service.tr("rs_rx")
        )
        self.layout.labelForField(self.rs_tx_input).setText(
            translation_service.tr("rs_tx")
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
