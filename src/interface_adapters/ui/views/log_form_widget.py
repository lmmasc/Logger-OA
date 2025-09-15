# Standard library imports
import uuid
import datetime
from domain.contact_type import ContactType

# Third-party imports
from PySide6.QtCore import Qt
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

# Local application imports
from translation.translation_service import translation_service
from interface_adapters.ui.view_manager import LogType, ViewID
from infrastructure.repositories.sqlite_radio_operator_repository import (
    SqliteRadioOperatorRepository,
)
from application.use_cases.operator_management import (
    get_operator_by_callsign,
    create_operator,
)
from application.use_cases.contact_management import (
    validate_contact_for_log,
    add_contact_to_log,
    find_duplicate_in_block,
)
from interface_adapters.ui.dialogs.operator_edit_dialog import OperatorEditDialog
from domain.repositories.contact_log_repository import ContactLogRepository


# Eliminado: ahora se importa desde domain.contact_type


class LogFormWidget(QWidget):
    """
    Widget base para formularios de contacto/log.
    Permite ingresar y gestionar datos de contacto para logs de operativos y concursos, con soporte multilenguaje.
    Reutilizable en operativos y concursos.
    """

    def __init__(self, parent=None, log_type=LogType.OPERATION_LOG):
        """
        Constructor principal del widget de formulario de log/contacto.
        Inicializa la instancia y configura la interfaz gráfica y el orden de tabulación.
        Args:
            parent: QWidget padre.
            log_type: Tipo de log (Enum LogType).
        """
        super().__init__(parent)
        self.log_type = log_type
        self._setup_ui()
        self._setup_tab_order()

    def _setup_ui(self):
        """
        Configura y construye la interfaz gráfica del formulario de log/contacto.
        Se definen los campos y etiquetas según el tipo de log (operativo o concurso).
        """
        main_layout = QVBoxLayout()
        main_layout.setSpacing(4)
        form_row = QHBoxLayout()
        form_row.setSpacing(8)
        form_row.setContentsMargins(0, 0, 0, 0)
        form_row.setAlignment(Qt.AlignLeft)
        # --- Bloque de campos para concursos ---
        if self.log_type == LogType.CONTEST_LOG:
            # RS_RX, intercambio recibido/enviado, RS_TX, observaciones
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
        # --- Bloque de campos para operativos ---
        else:
            # estación, energía, potencia, RS_RX, RS_TX, observaciones
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
        # --- Fin de definición de campos ---
        form_row_widget = QWidget(self)
        form_row_widget.setLayout(form_row)
        form_row_widget.setMinimumWidth(700)
        form_row_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.addWidget(form_row_widget)
        self.setLayout(main_layout)

    def _setup_tab_order(self):
        """
        Configura el orden de tabulación entre los campos del formulario.
        Se adapta según el tipo de log para mejorar la experiencia de usuario.
        """
        if self.log_type == LogType.CONTEST_LOG:
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
        Obtiene los datos ingresados en el formulario y los retorna como diccionario.
        Extrae y adapta los datos según el tipo de log (operativo o concurso).
        Args:
            callsign (str, opcional): Indicativo de llamada.
        Returns:
            dict: Datos del formulario, adaptados según el tipo de log.
        """
        callsign_val = callsign if callsign is not None else ""
        data = {
            "callsign": callsign_val,
            "rs_rx": self.rs_rx_input.text(),
            "rs_tx": self.rs_tx_input.text(),
            "region": "-",
        }
        if self.log_type == LogType.CONTEST_LOG:
            # --- Bloque de extracción de datos para concurso ---
            contact_id = str(uuid.uuid4())
            timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            operator = get_operator_by_callsign(callsign_val)
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
        elif self.log_type == LogType.OPERATION_LOG:
            # --- Bloque de extracción de datos para operativo ---
            operator = get_operator_by_callsign(callsign_val)
            name = operator.name if operator else ""
            country = operator.country if operator else ""
            region = operator.region if operator else "-"
            timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
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
        Permite acceder a la ventana principal para operaciones de actualización de UI y base de datos.
        Returns:
            MainWindow instance o None si no se encuentra.
        """
        parent = self.parent()
        while parent:
            if parent.__class__.__name__ == "MainWindow":
                return parent
            parent = parent.parent()
        return None

    def _on_add_contact(self, callsign=None):
        """
        Lógica principal para agregar un contacto al log actual.
        Incluye validación de datos, control de duplicados, actualización de la base de datos y UI, y manejo de diálogos de confirmación.
        Args:
            callsign (str, opcional): Indicativo de llamada a agregar.
        Returns:
            bool: True si el contacto fue agregado correctamente, False si hubo errores o cancelación.
        """
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
        # Validación de campos y control de foco
        operator = get_operator_by_callsign(callsign_val)
        main_window = self._find_main_window()
        db_path = getattr(main_window.current_log, "db_path", None)
        log_id = getattr(main_window.current_log, "id", None)
        contact_type = (
            ContactType.OPERATION
            if self.log_type == LogType.OPERATION_LOG
            else ContactType.CONTEST
        )
        repo_log = ContactLogRepository(db_path)
        contacts = repo_log.get_contacts(log_id)
        validation = validate_contact_for_log(
            data, contacts, contact_type, translation_service
        )
        if validation["errors"]:
            error_msg = translation_service.tr("contact_validation_error").format(
                error="; ".join(validation["errors"])
            )
            QMessageBox.critical(
                self,
                translation_service.tr("main_window_title"),
                error_msg,
            )
            # Asignar foco al campo correspondiente según el error
            focus_field = None
            field = validation["focus_field"]
            if field == "callsign_input" and hasattr(self.parent(), "callsign_input"):
                focus_field = self.parent().callsign_input.input
            elif hasattr(self, field):
                focus_field = getattr(self, field)
            if focus_field:
                focus_field.setFocus()
            return False
        # Validación de duplicados en bloque OA para concursos
        if contact_type == ContactType.CONTEST:
            duplicate = find_duplicate_in_block(
                data["callsign"], data["timestamp"], contacts
            )
            if duplicate:
                msg = (
                    f"El indicativo {duplicate['callsign']} ({duplicate['name']}) ya fue registrado en este bloque horario OA a las {duplicate['hora_oa']}. "
                    "¿Desea registrar de todas formas este contacto?"
                )
                reply = QMessageBox.question(
                    self,
                    translation_service.tr("main_window_title"),
                    msg,
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if reply != QMessageBox.Yes:
                    # Borrar campo de ingreso indicativo y dar foco
                    if hasattr(self.parent(), "callsign_input"):
                        self.parent().callsign_input.input.clear()
                        self.parent().callsign_input.input.setFocus()
                    return False
        # Si el operador existe, agregar contacto directamente
        if operator:
            try:
                add_contact_to_log(db_path, log_id, data, contact_type)
                contacts = repo_log.get_contacts(log_id)
                main_window.current_log.contacts = contacts
                # Actualiza la tabla y mueve el scroll en la vista correspondiente
                if hasattr(main_window, "view_manager"):
                    if (
                        self.log_type == LogType.OPERATION_LOG
                        and ViewID.LOG_OPS_VIEW in main_window.view_manager.views
                    ):
                        table_widget = main_window.view_manager.views[
                            ViewID.LOG_OPS_VIEW
                        ].table_widget
                        table_widget.set_contacts(contacts)
                        table = table_widget.table
                        table.scrollToBottom()
                        table.setFocus()
                        parent = self.parent()
                        while parent:
                            if hasattr(parent, "callsign_input"):
                                parent.callsign_input.input.clear()
                                parent.callsign_input.input.setFocus()
                                break
                            parent = parent.parent()
                    elif (
                        self.log_type == LogType.CONTEST_LOG
                        and ViewID.LOG_CONTEST_VIEW in main_window.view_manager.views
                    ):
                        table_widget = main_window.view_manager.views[
                            ViewID.LOG_CONTEST_VIEW
                        ].table_widget
                        table_widget.set_contacts(contacts)
                        table = table_widget.table
                        table.scrollToBottom()
                        table.setFocus()
                        parent = self.parent()
                        while parent:
                            if hasattr(parent, "callsign_input"):
                                parent.callsign_input.input.clear()
                                parent.callsign_input.input.setFocus()
                                break
                            parent = parent.parent()
                return True
            except Exception as e:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    str(e),
                )
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
                op_data = dlg.result_operator
                operator = create_operator(op_data)
                data["name"] = operator.name
                data["country"] = operator.country
                data["region"] = operator.region
        # Agregar contacto con los datos actuales (faltantes en blanco si no existe operador)
        try:
            add_contact_to_log(db_path, log_id, data, contact_type)
            contacts = repo_log.get_contacts(log_id)
            main_window.current_log.contacts = contacts
            if hasattr(main_window, "view_manager"):
                if (
                    self.log_type == LogType.OPERATION_LOG
                    and ViewID.LOG_OPS_VIEW in main_window.view_manager.views
                ):
                    table_widget = main_window.view_manager.views[
                        ViewID.LOG_OPS_VIEW
                    ].table_widget
                    table_widget.set_contacts(contacts)
                    table = table_widget.table
                    table.scrollToBottom()
                    table.setFocus()
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, "callsign_input"):
                            parent.callsign_input.input.clear()
                            parent.callsign_input.input.setFocus()
                            break
                        parent = parent.parent()
                elif (
                    self.log_type == LogType.CONTEST_LOG
                    and ViewID.LOG_CONTEST_VIEW in main_window.view_manager.views
                ):
                    table_widget = main_window.view_manager.views[
                        ViewID.LOG_CONTEST_VIEW
                    ].table_widget
                    table_widget.set_contacts(contacts)
                    table = table_widget.table
                    table.scrollToBottom()
                    table.setFocus()
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, "callsign_input"):
                            parent.callsign_input.input.clear()
                            parent.callsign_input.input.setFocus()
                            break
                        parent = parent.parent()
            return True
        except Exception as e:
            QMessageBox.critical(
                self,
                translation_service.tr("main_window_title"),
                str(e),
            )
            return False

    def retranslate_ui(self):
        """
        Actualiza los textos de la interfaz según el idioma seleccionado.
        Reasigna los textos de los labels y opciones de los selectores para reflejar el idioma actual.
        """
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
