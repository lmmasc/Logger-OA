from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
)
from translation.translation_service import translation_service
from PySide6.QtCore import Qt
import datetime


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log. Reutilizable en operativos y concursos.
    """

    def __init__(self, parent=None, log_type="ops"):
        super().__init__(parent)
        from .callsign_input_widget import CallsignInputWidget
        from PySide6.QtWidgets import (
            QPushButton,
            QMessageBox,
            QHBoxLayout,
            QVBoxLayout,
            QWidget,
            QGridLayout,
        )
        from PySide6.QtCore import QTimer

        self.log_type = log_type
        main_layout = QHBoxLayout(self)
        # Sección izquierda: formulario en dos columnas
        form_widget = QWidget(self)
        columns_layout = QHBoxLayout(form_widget)
        columns_layout.setContentsMargins(0, 0, 0, 0)
        # Primera columna
        col1 = QVBoxLayout()
        col1.setSpacing(4)
        # Segunda columna
        col2 = QVBoxLayout()
        col2.setSpacing(4)
        # Campo universal: Indicativo (arriba de todo, ocupa ambas columnas)
        self.callsign_input = CallsignInputWidget(self)
        columns_layout.addWidget(self.callsign_input)
        self.callsign_input.set_summary("", show_suggestions=True)
        self.callsign_input.suggestion_list.clear()

        # Helper para crear fila label-campo
        def add_row(layout, label_name, label_text, field):
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row.addWidget(label)
            row.addWidget(field)
            layout.addLayout(row)
            setattr(self, label_name, label)

        # Campos específicos según tipo de log (orden para operativos)
        if log_type == "ops":
            # Estación: selector
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
            add_row(
                col1,
                "station_label",
                translation_service.tr("station"),
                self.station_input,
            )
            # Energía: selector
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
            add_row(
                col1,
                "energy_label",
                translation_service.tr("energy"),
                self.energy_input,
            )
            # Potencia: valor por defecto 1
            self.power_input = QLineEdit(self)
            self.power_input.setText("1")
            add_row(
                col1, "power_label", translation_service.tr("power"), self.power_input
            )
        # Segunda columna: RS_RX, RS_TX, Observaciones
        self.rs_rx_input = QLineEdit(self)
        self.rs_rx_input.setText("59")
        add_row(col2, "rs_rx_label", translation_service.tr("rs_rx"), self.rs_rx_input)
        self.rs_tx_input = QLineEdit(self)
        self.rs_tx_input.setText("59")
        add_row(col2, "rs_tx_label", translation_service.tr("rs_tx"), self.rs_tx_input)
        self.observations_input = QLineEdit(self)
        add_row(
            col2,
            "observations_label",
            translation_service.tr("observations"),
            self.observations_input,
        )
        # Campos específicos para concursos
        if log_type == "contest":
            self.exchange_received_input = QLineEdit(self)
            add_row(
                col2,
                "exchange_received_label",
                translation_service.tr("exchange_received"),
                self.exchange_received_input,
            )
            self.exchange_sent_input = QLineEdit(self)
            add_row(
                col2,
                "exchange_sent_label",
                translation_service.tr("exchange_sent"),
                self.exchange_sent_input,
            )
        # Añadir columnas al layout
        columns_layout.addLayout(col1)
        columns_layout.addLayout(col2)
        form_widget.setLayout(columns_layout)
        main_layout.addWidget(form_widget, 3)
        # Sección derecha: relojes
        clock_widget = QWidget(self)
        clock_layout = QHBoxLayout(clock_widget)
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_layout.setSpacing(16)
        # Subwidget OA
        oa_box = QVBoxLayout()
        oa_box.setSpacing(2)
        self.oa_label = QLabel(self)
        self.oa_time = QLabel(self)
        self.oa_date = QLabel(self)
        self.oa_label.setText(translation_service.tr("clock_oa_label"))
        self.oa_label.setAlignment(Qt.AlignCenter)
        self.oa_time.setAlignment(Qt.AlignCenter)
        self.oa_date.setAlignment(Qt.AlignCenter)
        self.oa_time.setStyleSheet("color: red; font-size: 30px; font-weight: bold;")
        self.oa_label.setStyleSheet("color: red; font-weight: bold;")
        self.oa_date.setStyleSheet("color: red;")
        oa_box.addWidget(self.oa_label)
        oa_box.addWidget(self.oa_time)
        oa_box.addWidget(self.oa_date)
        oa_widget = QWidget(self)
        oa_widget.setLayout(oa_box)
        # Subwidget UTC
        utc_box = QVBoxLayout()
        utc_box.setSpacing(2)
        self.utc_label = QLabel(self)
        self.utc_time = QLabel(self)
        self.utc_date = QLabel(self)
        self.utc_label.setText(translation_service.tr("clock_utc_label"))
        self.utc_label.setAlignment(Qt.AlignCenter)
        self.utc_time.setAlignment(Qt.AlignCenter)
        self.utc_date.setAlignment(Qt.AlignCenter)
        self.utc_time.setStyleSheet("color: green; font-size: 30px; font-weight: bold;")
        self.utc_label.setStyleSheet("color: green; font-weight: bold;")
        self.utc_date.setStyleSheet("color: green;")
        utc_box.addWidget(self.utc_label)
        utc_box.addWidget(self.utc_time)
        utc_box.addWidget(self.utc_date)
        utc_widget = QWidget(self)
        utc_widget.setLayout(utc_box)
        # Añadir ambos al layout horizontal
        clock_layout.addWidget(oa_widget)
        clock_layout.addWidget(utc_widget)
        clock_widget.setLayout(clock_layout)
        main_layout.insertWidget(1, clock_widget, 1)
        # Timer para actualizar los relojes
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clocks)
        self._clock_timer.start(1000)
        # Sección final: botones
        button_widget = QWidget(self)
        button_layout = QVBoxLayout(button_widget)
        self.add_contact_btn = QPushButton(translation_service.tr("add_contact"), self)
        button_layout.addWidget(self.add_contact_btn)
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget, 1)
        self.setLayout(main_layout)

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
        self.callsign_input.retranslate_ui()
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
        self.oa_label.setText(translation_service.tr("clock_oa_label"))
        self.utc_label.setText(translation_service.tr("clock_utc_label"))

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

    def _update_clocks(self):
        now = datetime.datetime.now()
        now_utc = datetime.datetime.utcnow()
        lang = translation_service.get_language()
        if lang == "es":
            date_fmt = "%d/%m/%Y"
        else:
            date_fmt = "%m/%d/%Y"
        self.oa_time.setText(now.strftime("%H:%M:%S"))
        self.oa_date.setText(now.strftime(date_fmt))
        self.utc_time.setText(now_utc.strftime("%H:%M:%S"))
        self.utc_date.setText(now_utc.strftime(date_fmt))
