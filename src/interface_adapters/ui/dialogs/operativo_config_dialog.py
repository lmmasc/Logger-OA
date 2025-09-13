# Dialogo de configuración de log operativo
# Permite seleccionar tipo de operativo, banda, modo, frecuencia y repetidora
# Autor: (tu nombre o equipo)
# Fecha: 2025-09-11

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class OperativoConfigDialog(QDialog):
    """
    Diálogo para configurar los parámetros de un log operativo.
    Permite seleccionar tipo de operativo, banda, modo, frecuencia y repetidora.
    La lógica dinámica ajusta los campos según la selección del usuario.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("operation_config_title"))
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)

        # Tipo de operativo
        self.operation_type_label = QLabel(
            translation_service.tr("operation_type_label")
        )
        self.operation_type_combo = QComboBox(self)
        self.operation_type_keys = [
            "cps_operation",
            "rener_operation",
            "bulletin_operation",
            "generic_operation",
        ]
        self.operation_type_combo.addItems(
            [translation_service.tr(k) for k in self.operation_type_keys]
        )
        layout.addWidget(self.operation_type_label)
        layout.addWidget(self.operation_type_combo)

        # Banda de frecuencia
        self.frequency_band_label = QLabel(
            translation_service.tr("operation_band_label")
        )
        self.frequency_band_combo = QComboBox(self)
        self.frequency_band_keys = ["band_hf", "band_vhf", "band_uhf"]
        self.frequency_band_combo.addItems(
            [translation_service.tr(k) for k in self.frequency_band_keys]
        )
        layout.addWidget(self.frequency_band_label)
        layout.addWidget(self.frequency_band_combo)

        # Modo de operación
        self.modo_label = QLabel(translation_service.tr("operation_mode_label"))
        self.modo_combo = QComboBox(self)
        self.modo_keys = ["mode_lsb", "mode_usb", "mode_fm", "mode_other"]
        self.modo_combo.addItems([translation_service.tr(k) for k in self.modo_keys])
        layout.addWidget(self.modo_label)
        layout.addWidget(self.modo_combo)

        # Repetidora (solo VHF)
        self.rep_label = QLabel(translation_service.tr("operation_rep_label"))
        self.rep_combo = QComboBox(self)
        self.rep_keys = ["rep_simplex", "rep_r1", "rep_r2", "rep_r3"]
        self.rep_combo.addItems([translation_service.tr(k) for k in self.rep_keys])
        layout.addWidget(self.rep_label)
        layout.addWidget(self.rep_combo)
        self.rep_label.hide()
        self.rep_combo.hide()

        # Frecuencia (después de repetidora)
        self.freq_label = QLabel(translation_service.tr("operation_freq_label"))
        self.freq_edit = QLineEdit(self)
        layout.addWidget(self.freq_label)
        layout.addWidget(self.freq_edit)

        # Botón OK
        self.ok_btn = QPushButton(translation_service.tr("ok_button"), self)
        layout.addWidget(self.ok_btn)
        self.ok_btn.clicked.connect(self.accept)

        # Conexión de lógica dinámica
        self.operation_type_combo.currentIndexChanged.connect(self._update_fields)
        self.frequency_band_combo.currentIndexChanged.connect(self._update_fields)
        self.rep_combo.currentIndexChanged.connect(self._update_fields)
        self._update_fields()

        # Asegurar que el combo de repetidora tenga siempre una opción seleccionada por defecto ('rep_simplex')
        self.rep_combo.setCurrentIndex(0)

    def _update_fields(self):
        """
        Actualiza los campos dinámicamente según el tipo de operativo y banda seleccionados.
        - CPS: solo HF, modo LSB, frecuencia 7100
        - RENER: si HF, frecuencia 7100
        - VHF: muestra repetidora y ajusta frecuencia según repetidora
        """
        operation_type = self.operation_type_keys[
            self.operation_type_combo.currentIndex()
        ]
        frequency_band = self.frequency_band_keys[
            self.frequency_band_combo.currentIndex()
        ]
        if operation_type == "cps_operation":
            self.frequency_band_combo.setCurrentIndex(0)  # HF
            self.frequency_band_combo.setEnabled(False)
            self.modo_combo.setCurrentIndex(0)  # LSB
            self.freq_edit.setText("7100")
            self.rep_label.hide()
            self.rep_combo.hide()
            self.freq_label.show()
            self.freq_edit.setEnabled(True)
        else:
            self.frequency_band_combo.setEnabled(True)
            if frequency_band == "band_hf":
                self.modo_combo.setCurrentIndex(0)  # LSB
                self.rep_label.hide()
                self.rep_combo.hide()
                self.freq_label.show()
                self.freq_edit.setEnabled(True)
                if operation_type == "rener_operation":
                    self.freq_edit.setText("7100")
                else:
                    self.freq_edit.setText("")
            elif frequency_band == "band_vhf":
                self.modo_combo.setCurrentIndex(2)  # FM
                self.rep_label.show()
                self.rep_combo.show()
                self.freq_label.show()
                rep = self.rep_keys[self.rep_combo.currentIndex()]
                if rep == "rep_r1":
                    self.freq_edit.setText("146960")
                    self.freq_edit.setEnabled(False)
                elif rep == "rep_r2":
                    self.freq_edit.setText("147050")
                    self.freq_edit.setEnabled(False)
                elif rep == "rep_r3":
                    self.freq_edit.setText("146880")
                    self.freq_edit.setEnabled(False)
                else:  # Simplex
                    self.freq_edit.setText("146520")
                    self.freq_edit.setEnabled(True)
            else:
                self.modo_combo.setCurrentIndex(3)  # Otro
                self.rep_label.hide()
                self.rep_combo.hide()
                self.freq_label.show()
                self.freq_edit.setEnabled(True)
                self.freq_edit.setText("")

    def get_config(self):
        """
        Devuelve la configuración seleccionada en el diálogo como diccionario.
        Claves:
            - operation_type: tipo de operativo
            - frequency_band: banda seleccionada
            - mode_key: modo de operación
            - frequency: frecuencia
            - repeater_key: repetidora (si aplica)
        """
        return {
            "operation_type": self.operation_type_keys[
                self.operation_type_combo.currentIndex()
            ],
            "frequency_band": self.frequency_band_keys[
                self.frequency_band_combo.currentIndex()
            ],
            "mode_key": self.modo_keys[self.modo_combo.currentIndex()],
            "frequency": self.freq_edit.text(),
            "repeater_key": (
                self.rep_keys[self.rep_combo.currentIndex()]
                if self.frequency_band_combo.currentText()
                == translation_service.tr("band_vhf")
                else None
            ),
        }
