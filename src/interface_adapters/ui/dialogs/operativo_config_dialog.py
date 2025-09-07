from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class OperativoConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("operativo_config_title"))
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)

        # Tipo de operativo
        self.tipo_label = QLabel(translation_service.tr("operativo_type_label"))
        self.tipo_combo = QComboBox(self)
        self.tipo_keys = [
            "operativo_cps",
            "operativo_rener",
            "operativo_boletin",
            "operativo_generico",
        ]
        self.tipo_combo.addItems([translation_service.tr(k) for k in self.tipo_keys])
        layout.addWidget(self.tipo_label)
        layout.addWidget(self.tipo_combo)

        # Banda
        self.banda_label = QLabel(translation_service.tr("operativo_band_label"))
        self.banda_combo = QComboBox(self)
        self.banda_keys = ["band_hf", "band_vhf", "band_uhf"]
        self.banda_combo.addItems([translation_service.tr(k) for k in self.banda_keys])
        layout.addWidget(self.banda_label)
        layout.addWidget(self.banda_combo)

        # Modo
        self.modo_label = QLabel(translation_service.tr("operativo_mode_label"))
        self.modo_combo = QComboBox(self)
        self.modo_keys = ["mode_lsb", "mode_usb", "mode_fm", "mode_other"]
        self.modo_combo.addItems([translation_service.tr(k) for k in self.modo_keys])
        layout.addWidget(self.modo_label)
        layout.addWidget(self.modo_combo)

        # Frecuencia
        self.freq_label = QLabel(translation_service.tr("operativo_freq_label"))
        self.freq_edit = QLineEdit(self)
        layout.addWidget(self.freq_label)
        layout.addWidget(self.freq_edit)

        # Repetidora (solo VHF)
        self.rep_label = QLabel(translation_service.tr("operativo_rep_label"))
        self.rep_combo = QComboBox(self)
        self.rep_keys = ["rep_simplex", "rep_r1", "rep_r2", "rep_r3"]
        self.rep_combo.addItems([translation_service.tr(k) for k in self.rep_keys])
        layout.addWidget(self.rep_label)
        layout.addWidget(self.rep_combo)
        self.rep_label.hide()
        self.rep_combo.hide()

        # Botón OK
        self.ok_btn = QPushButton(translation_service.tr("ok_button"), self)
        layout.addWidget(self.ok_btn)
        self.ok_btn.clicked.connect(self.accept)

        # Lógica dinámica
        self.tipo_combo.currentIndexChanged.connect(self._update_fields)
        self.banda_combo.currentIndexChanged.connect(self._update_fields)
        self.rep_combo.currentIndexChanged.connect(self._update_fields)
        self._update_fields()

    def _update_fields(self):
        tipo = self.tipo_keys[self.tipo_combo.currentIndex()]
        banda = self.banda_keys[self.banda_combo.currentIndex()]
        # CPS solo HF
        if tipo == "operativo_cps":
            self.banda_combo.setCurrentIndex(0)  # HF
            self.banda_combo.setEnabled(False)
            self.modo_combo.setCurrentIndex(0)  # LSB
            self.freq_edit.setText("7100")
            self.rep_label.hide()
            self.rep_combo.hide()
        else:
            self.banda_combo.setEnabled(True)
            if banda == "band_hf":
                self.modo_combo.setCurrentIndex(0)  # LSB
                self.rep_label.hide()
                self.rep_combo.hide()
                if tipo == "operativo_rener":
                    self.freq_edit.setText("7100")
                else:
                    self.freq_edit.setText("")
            elif banda == "band_vhf":
                self.modo_combo.setCurrentIndex(2)  # FM
                self.rep_label.show()
                self.rep_combo.show()
                rep = self.rep_keys[self.rep_combo.currentIndex()]
                if rep == "rep_r1":
                    self.freq_edit.setText("146960")
                elif rep == "rep_r2":
                    self.freq_edit.setText("147050")
                elif rep == "rep_r3":
                    self.freq_edit.setText("146880")
                else:
                    self.freq_edit.setText("")
            else:
                self.modo_combo.setCurrentIndex(3)  # Otro
                self.rep_label.hide()
                self.rep_combo.hide()
                self.freq_edit.setText("")

    def get_config(self):
        return {
            "tipo_key": self.tipo_keys[self.tipo_combo.currentIndex()],
            "banda_key": self.banda_keys[self.banda_combo.currentIndex()],
            "modo_key": self.modo_keys[self.modo_combo.currentIndex()],
            "frecuencia": self.freq_edit.text(),
            "repetidora_key": (
                self.rep_keys[self.rep_combo.currentIndex()]
                if self.rep_combo.isVisible()
                else None
            ),
        }
