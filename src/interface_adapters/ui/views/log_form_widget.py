from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
import datetime
from infrastructure.repositories.sqlite_radio_operator_repository import (
    SqliteRadioOperatorRepository,
)


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log. Reutilizable en operativos y concursos.
    Permite ingresar y gestionar datos de contacto para logs de operativos y concursos, con soporte multilenguaje.
    """

    def __init__(
        self,
        parent=None,
        log_type="ops",
        callsign="",
        log_type_name="",
        log_date="",
    ):
        """
        Inicializa el formulario de log/contacto.
        Args:
            parent: QWidget padre.
            log_type: Tipo de log ('ops' o 'contest').
            callsign: Indicativo de llamada.
            log_type_name: Nombre del tipo de log.
            log_date: Fecha del log.
        """
        super().__init__(parent)

        # Anchos fijos para los labels (ajustar manualmente si es necesario)
        self.log_type = log_type
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(4)

        # --- Formulario horizontal ---
        form_row = QHBoxLayout()
        form_row.setSpacing(8)
        form_row.setContentsMargins(0, 0, 0, 0)
        form_row.setAlignment(Qt.AlignLeft)

        if self.log_type == "contest":
            # RS_RX
            self.rs_rx_input = QLineEdit(self)
            self.rs_rx_input.setText("59")
            self.rs_rx_input.setFixedWidth(50)
            self.rs_rx_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            rs_rx_label = QLabel(translation_service.tr("rs_rx"))
            rs_rx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            rs_rx_label.setFixedWidth(50)
            rs_rx_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(rs_rx_label)
            form_row.addWidget(self.rs_rx_input)
            self.rs_rx_label = rs_rx_label

            # Intercambio recibido
            self.exchange_received_input = QLineEdit(self)
            self.exchange_received_input.setFixedWidth(80)
            self.exchange_received_input.setSizePolicy(
                QSizePolicy.Fixed, QSizePolicy.Fixed
            )
            exchange_received_label = QLabel(
                translation_service.tr("exchange_received")
            )
            exchange_received_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            exchange_received_label.setFixedWidth(140)
            exchange_received_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(exchange_received_label)
            form_row.addWidget(self.exchange_received_input)
            self.exchange_received_label = exchange_received_label

            # RS_TX
            self.rs_tx_input = QLineEdit(self)
            self.rs_tx_input.setText("59")
            self.rs_tx_input.setFixedWidth(50)
            self.rs_tx_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            rs_tx_label = QLabel(translation_service.tr("rs_tx"))
            rs_tx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            rs_tx_label.setFixedWidth(50)
            rs_tx_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(rs_tx_label)
            form_row.addWidget(self.rs_tx_input)
            self.rs_tx_label = rs_tx_label

            # Intercambio enviado
            self.exchange_sent_input = QLineEdit(self)
            self.exchange_sent_input.setFixedWidth(80)
            self.exchange_sent_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            exchange_sent_label = QLabel(translation_service.tr("exchange_sent"))
            exchange_sent_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            exchange_sent_label.setFixedWidth(140)
            exchange_sent_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(exchange_sent_label)
            form_row.addWidget(self.exchange_sent_input)
            self.exchange_sent_label = exchange_sent_label

            # Observaciones (expansivo)
            self.observations_input = QLineEdit(self)
            self.observations_input.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Fixed
            )
            obs_label = QLabel(translation_service.tr("observations"))
            obs_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            obs_label.setFixedWidth(40)
            obs_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(obs_label)
            form_row.addWidget(self.observations_input, 1)
            self.observations_label = obs_label
        else:
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
            self.station_input.setFixedWidth(120)
            self.station_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            station_label = QLabel(translation_service.tr("station"))
            station_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            station_label.setFixedWidth(60)
            station_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
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
            self.energy_input.setFixedWidth(120)
            self.energy_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            energy_label = QLabel(translation_service.tr("energy"))
            energy_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            energy_label.setFixedWidth(60)
            energy_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(energy_label)
            form_row.addWidget(self.energy_input)
            self.energy_label = energy_label

            # Power
            self.power_input = QLineEdit(self)
            self.power_input.setText("1")
            self.power_input.setFixedWidth(60)
            self.power_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            power_label = QLabel(f"{translation_service.tr('power')} (W)")
            power_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            power_label.setFixedWidth(90)
            power_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(power_label)
            form_row.addWidget(self.power_input)
            self.power_label = power_label

            # RS_RX
            self.rs_rx_input = QLineEdit(self)
            self.rs_rx_input.setText("59")
            self.rs_rx_input.setFixedWidth(50)
            self.rs_rx_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            rs_rx_label = QLabel(translation_service.tr("rs_rx"))
            rs_rx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            rs_rx_label.setFixedWidth(50)
            rs_rx_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(rs_rx_label)
            form_row.addWidget(self.rs_rx_input)
            self.rs_rx_label = rs_rx_label

            # RS_TX
            self.rs_tx_input = QLineEdit(self)
            self.rs_tx_input.setText("59")
            self.rs_tx_input.setFixedWidth(50)
            self.rs_tx_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            rs_tx_label = QLabel(translation_service.tr("rs_tx"))
            rs_tx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            rs_tx_label.setFixedWidth(50)
            rs_tx_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(rs_tx_label)
            form_row.addWidget(self.rs_tx_input)
            self.rs_tx_label = rs_tx_label

            # Observaciones (expansivo)
            self.observations_input = QLineEdit(self)
            self.observations_input.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Fixed
            )
            obs_label = QLabel(translation_service.tr("observations"))
            obs_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            obs_label.setFixedWidth(40)
            obs_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            form_row.addWidget(obs_label)
            form_row.addWidget(
                self.observations_input, 1
            )  # stretch factor 1 para ocupar espacio restante
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

        # Refuerzo de tabulación solo entre campos internos
        if self.log_type == "contest":
            QWidget.setTabOrder(self.rs_rx_input, self.exchange_received_input)
            QWidget.setTabOrder(self.exchange_received_input, self.rs_tx_input)
            QWidget.setTabOrder(self.rs_tx_input, self.exchange_sent_input)
            QWidget.setTabOrder(self.exchange_sent_input, self.observations_input)
        else:
            QWidget.setTabOrder(self.station_input, self.energy_input)
            QWidget.setTabOrder(self.energy_input, self.power_input)
            QWidget.setTabOrder(self.power_input, self.rs_rx_input)
            QWidget.setTabOrder(self.rs_rx_input, self.rs_tx_input)
            QWidget.setTabOrder(self.rs_tx_input, self.observations_input)

    def get_data(self, callsign=None):
        """
        Devuelve los datos del formulario como diccionario.
        Args:
            callsign (str, opcional): Indicativo de llamada.
        Returns:
            dict: Datos del formulario.
        """
        callsign_val = callsign if callsign is not None else ""
        data = {
            "callsign": callsign_val,
            "rs_rx": self.rs_rx_input.text(),
            "rs_tx": self.rs_tx_input.text(),
            "region": "-",
        }
        if self.log_type == "contest":
            import uuid

            contact_id = str(uuid.uuid4())
            timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            repo = SqliteRadioOperatorRepository()
            operator = repo.get_operator_by_callsign(callsign_val)
            name = operator.name if operator else "-"
            region = operator.region if operator else "-"
            data.update(
                {
                    "id": contact_id,
                    "name": name,
                    "region": region,
                    "exchange_received": self.exchange_received_input.text(),
                    "exchange_sent": self.exchange_sent_input.text(),
                    "rs_rx": self.rs_rx_input.text(),
                    "rs_tx": self.rs_tx_input.text(),
                    "observations": self.observations_input.text(),
                    "block": 1,
                    "points": 0,
                    "timestamp": timestamp,
                }
            )
        elif self.log_type == "ops":
            repo = SqliteRadioOperatorRepository()
            operator = repo.get_operator_by_callsign(callsign_val)
            name = operator.name if operator else ""
            country = operator.country if operator else ""
            region = operator.region if operator else "-"
            timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            # Definir las keys en el mismo orden que los textos
            station_keys = [
                "no_data",
                "station_base",
                "station_mobile",
                "station_portable",
            ]
            energy_keys = [
                "no_data",
                "energy_autonomous",
                "energy_battery",
                "energy_commercial",
            ]
            station_key = (
                station_keys[self.station_input.currentIndex()]
                if self.station_input
                else ""
            )
            energy_key = (
                energy_keys[self.energy_input.currentIndex()]
                if self.energy_input
                else ""
            )
            import uuid

            contact_id = str(uuid.uuid4())
            data.update(
                {
                    "id": contact_id,
                    "name": name,
                    "country": country,
                    "region": region,
                    "station": station_key,
                    "energy": energy_key,
                    "power": self.power_input.text(),
                    "timestamp": timestamp,
                    "obs": self.observations_input.text(),
                }
            )

        return data

    def _find_main_window(self):
        """
        Busca la instancia de MainWindow en la jerarquía de padres.
        Returns:
            MainWindow instance o None
        """
        # Busca la instancia de MainWindow en la jerarquía de padres
        parent = self.parent()
        while parent:
            if parent.__class__.__name__ == "MainWindow":
                return parent
            parent = parent.parent()
        return None

    def _on_add_contact(self, callsign=None):
        from infrastructure.repositories.sqlite_radio_operator_repository import (
            SqliteRadioOperatorRepository,
        )
        from PySide6.QtWidgets import QMessageBox
        from interface_adapters.ui.dialogs.operator_edit_dialog import (
            OperatorEditDialog,
        )

        repo = SqliteRadioOperatorRepository()
        # Obtener el valor de callsign directamente del campo si no se pasa como argumento
        callsign_val = (
            callsign
            if callsign is not None
            else (
                self.parent().callsign_input.get_callsign().strip()
                if hasattr(self.parent(), "callsign_input")
                else ""
            )
        )
        data = self.get_data(callsign_val)
        if callsign_val:
            data["callsign"] = callsign_val
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
        # Verificar si el indicativo existe en la base de datos usando el valor correcto
        operator = repo.get_operator_by_callsign(callsign_val)
        if operator:
            # Indicativo existe: agregar contacto y mover scroll
            try:
                from application.use_cases.contact_management import add_contact_to_log
                from domain.repositories.contact_log_repository import (
                    ContactLogRepository,
                )

                contact = add_contact_to_log(db_path, log_id, data, contact_type)
                repo_log = ContactLogRepository(db_path)
                contacts = repo_log.get_contacts(log_id)
                main_window.current_log.contacts = contacts
                # Actualiza la tabla y mueve el scroll
                if hasattr(main_window, "view_manager"):
                    if (
                        self.log_type == "ops"
                        and "log_ops" in main_window.view_manager.views
                    ):
                        table_widget = main_window.view_manager.views[
                            "log_ops"
                        ].table_widget
                        table = table_widget.table
                        table_widget.set_contacts(contacts)
                        table.scrollToBottom()
                        table.setFocus()
                        parent = self.parent()
                        while parent:
                            if hasattr(parent, "callsign_input"):
                                # Limpiar campo y mover foco solo si se agregó correctamente
                                parent.callsign_input.input.clear()
                                parent.callsign_input.input.setFocus()
                                break
                            parent = parent.parent()
                    elif (
                        self.log_type == "contest"
                        and "log_contest" in main_window.view_manager.views
                    ):
                        table_widget = main_window.view_manager.views[
                            "log_contest"
                        ].table_widget
                        table = table_widget.table
                        table_widget.set_contacts(contacts)
                        table.scrollToBottom()
                        table.setFocus()
                        parent = self.parent()
                        while parent:
                            if hasattr(parent, "callsign_input"):
                                # Limpiar campo y mover foco solo si se agregó correctamente
                                parent.callsign_input.input.clear()
                                parent.callsign_input.input.setFocus()
                                break
                            parent = parent.parent()
                # Si todo fue exitoso
                return True
            except Exception as e:
                raw_errors = str(e).split(";")
                translated_errors = []
                focus_field = None
                for err in raw_errors:
                    err = err.strip()
                    if err == "Missing received exchange.":
                        translated_errors.append(
                            translation_service.tr(
                                "validation_missing_received_exchange"
                            )
                        )
                        if focus_field is None:
                            focus_field = self.exchange_received_input
                    elif err == "Missing sent exchange.":
                        translated_errors.append(
                            translation_service.tr("validation_missing_sent_exchange")
                        )
                        if focus_field is None:
                            focus_field = self.exchange_sent_input
                    elif err.startswith("Duplicate contact"):
                        translated_errors.append(
                            translation_service.tr("validation_duplicate_contact")
                        )
                        if focus_field is None:
                            focus_field = (
                                self.parent().callsign_input.input
                                if hasattr(self.parent(), "callsign_input")
                                else None
                            )
                    elif err.startswith("Invalid callsign"):
                        callsign = err.split(":", 1)[-1].strip()
                        translated_errors.append(
                            translation_service.tr(
                                "validation_invalid_callsign"
                            ).format(callsign=callsign)
                        )
                        if focus_field is None:
                            focus_field = (
                                self.parent().callsign_input.input
                                if hasattr(self.parent(), "callsign_input")
                                else None
                            )
                    elif err.startswith("Invalid time format"):
                        time = err.split(":", 1)[-1].strip()
                        translated_errors.append(
                            translation_service.tr(
                                "validation_invalid_time_format"
                            ).format(time=time)
                        )
                        # No hay campo específico, mantener foco
                    elif err == "Missing station.":
                        translated_errors.append(
                            translation_service.tr("validation_missing_station")
                        )
                        if focus_field is None and hasattr(self, "station_input"):
                            focus_field = self.station_input
                    elif err.startswith("Invalid power value"):
                        power = err.split(":", 1)[-1].strip()
                        translated_errors.append(
                            translation_service.tr(
                                "validation_invalid_power_value"
                            ).format(power=power)
                        )
                        if focus_field is None and hasattr(self, "power_input"):
                            focus_field = self.power_input
                    elif err == "Missing RS_RX.":
                        translated_errors.append(
                            translation_service.tr("validation_missing_rs_rx")
                        )
                        if focus_field is None:
                            focus_field = self.rs_rx_input
                    elif err == "Missing RS_TX.":
                        translated_errors.append(
                            translation_service.tr("validation_missing_rs_tx")
                        )
                        if focus_field is None:
                            focus_field = self.rs_tx_input
                    else:
                        translated_errors.append(err)
                error_msg = translation_service.tr("contact_validation_error").format(
                    error="; ".join(translated_errors)
                )
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    error_msg,
                )
                # Si se identificó el campo, mover el foco SOLO al primero
                if focus_field:
                    focus_field.setFocus()
                return False
        # Si no existe, preguntar si desea agregarlo a la base de datos
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(translation_service.tr("add_operator"))
        msg_box.setText(translation_service.tr("operator_not_found_msg"))
        msg_box.setInformativeText(
            f"{translation_service.tr('table_header_callsign')}: {callsign}"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText(translation_service.tr("yes_button"))
        msg_box.button(QMessageBox.No).setText(translation_service.tr("no_button"))
        reply = msg_box.exec()
        if reply == QMessageBox.Yes:
            # Abrir diálogo para agregar operador
            dlg = OperatorEditDialog(parent=self)
            dlg.inputs["callsign"].setText(callsign)
            if dlg.exec() == QMessageBox.Accepted and dlg.result_operator:
                # Agregar operador a la base de datos
                from domain.entities.radio_operator import RadioOperator

                op_data = dlg.result_operator
                # Mapear claves 'type' y 'license' a 'type_' y 'license_'
                if "type" in op_data:
                    op_data["type_"] = op_data.pop("type")
                if "license" in op_data:
                    op_data["license_"] = op_data.pop("license")
                new_operator = RadioOperator(**op_data)
                repo.add(new_operator)
                # Recargar base de datos y agregar contacto
                operator = repo.get_operator_by_callsign(callsign)
                data["name"] = operator.name
                data["country"] = operator.country
                data["region"] = operator.region
        # Agregar contacto con los datos actuales (faltantes en blanco si no existe operador)
        try:
            from application.use_cases.contact_management import add_contact_to_log
            from domain.repositories.contact_log_repository import ContactLogRepository

            contact = add_contact_to_log(db_path, log_id, data, contact_type)
            repo_log = ContactLogRepository(db_path)
            contacts = repo_log.get_contacts(log_id)
            main_window.current_log.contacts = contacts
            # Actualiza la tabla y mueve el scroll
            if hasattr(main_window, "view_manager"):
                if (
                    self.log_type == "ops"
                    and "log_ops" in main_window.view_manager.views
                ):
                    table_widget = main_window.view_manager.views[
                        "log_ops"
                    ].table_widget
                    table = table_widget.table
                    table_widget.set_contacts(contacts)
                    table.scrollToBottom()
                    table.setFocus()
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, "callsign_input"):
                            # Limpiar campo y mover foco solo si se agregó correctamente
                            parent.callsign_input.input.clear()
                            parent.callsign_input.input.setFocus()
                            break
                        parent = parent.parent()
                elif (
                    self.log_type == "contest"
                    and "log_contest" in main_window.view_manager.views
                ):
                    table_widget = main_window.view_manager.views[
                        "log_contest"
                    ].table_widget
                    table = table_widget.table
                    table_widget.set_contacts(contacts)
                    table.scrollToBottom()
                    table.setFocus()
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, "callsign_input"):
                            # Limpiar campo y mover foco solo si se agregó correctamente
                            parent.callsign_input.input.clear()
                            parent.callsign_input.input.setFocus()
                            break
                        parent = parent.parent()
            # Si todo fue exitoso
            return True
        except Exception as e:
            raw_errors = str(e).split(";")
            translated_errors = []
            focus_field = None
            for err in raw_errors:
                err = err.strip()
                if err == "Missing received exchange.":
                    translated_errors.append(
                        translation_service.tr("validation_missing_received_exchange")
                    )
                    if focus_field is None:
                        focus_field = self.exchange_received_input
                elif err == "Missing sent exchange.":
                    translated_errors.append(
                        translation_service.tr("validation_missing_sent_exchange")
                    )
                    if focus_field is None:
                        focus_field = self.exchange_sent_input
                elif err.startswith("Duplicate contact"):
                    translated_errors.append(
                        translation_service.tr("validation_duplicate_contact")
                    )
                    if focus_field is None:
                        focus_field = (
                            self.parent().callsign_input.input
                            if hasattr(self.parent(), "callsign_input")
                            else None
                        )
                elif err.startswith("Invalid callsign"):
                    callsign = err.split(":", 1)[-1].strip()
                    translated_errors.append(
                        translation_service.tr("validation_invalid_callsign").format(
                            callsign=callsign
                        )
                    )
                    if focus_field is None:
                        focus_field = (
                            self.parent().callsign_input.input
                            if hasattr(self.parent(), "callsign_input")
                            else None
                        )
                elif err.startswith("Invalid time format"):
                    time = err.split(":", 1)[-1].strip()
                    translated_errors.append(
                        translation_service.tr("validation_invalid_time_format").format(
                            time=time
                        )
                    )
                    # No hay campo específico, mantener foco
                elif err == "Missing station.":
                    translated_errors.append(
                        translation_service.tr("validation_missing_station")
                    )
                    if focus_field is None and hasattr(self, "station_input"):
                        focus_field = self.station_input
                elif err.startswith("Invalid power value"):
                    power = err.split(":", 1)[-1].strip()
                    translated_errors.append(
                        translation_service.tr("validation_invalid_power_value").format(
                            power=power
                        )
                    )
                    if focus_field is None and hasattr(self, "power_input"):
                        focus_field = self.power_input
                elif err == "Missing RS_RX.":
                    translated_errors.append(
                        translation_service.tr("validation_missing_rs_rx")
                    )
                    if focus_field is None:
                        focus_field = self.rs_rx_input
                elif err == "Missing RS_TX.":
                    translated_errors.append(
                        translation_service.tr("validation_missing_rs_tx")
                    )
                    if focus_field is None:
                        focus_field = self.rs_tx_input
                else:
                    translated_errors.append(err)
            error_msg = translation_service.tr("contact_validation_error").format(
                error="; ".join(translated_errors)
            )
            QMessageBox.critical(
                self,
                translation_service.tr("main_window_title"),
                error_msg,
            )
            # Si se identificó el campo, mover el foco SOLO al primero
            if focus_field:
                focus_field.setFocus()
            return False

    def retranslate_ui(self):
        """
        Actualiza los textos de la interfaz según el idioma seleccionado.
        """
        # Actualizar todos los labels manualmente por el nuevo layout
        if hasattr(self, "station_label"):
            self.station_label.setText(translation_service.tr("station"))
        if hasattr(self, "energy_label"):
            self.energy_label.setText(translation_service.tr("energy"))
        if hasattr(self, "power_label"):
            self.power_label.setText(f"{translation_service.tr('power')} (W)")
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
