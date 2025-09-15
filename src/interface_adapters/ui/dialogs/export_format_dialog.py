"""
ExportFormatDialog
Diálogo para seleccionar el formato de exportación de log.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from translation.translation_service import translation_service
from interface_adapters.ui.view_manager import LogType


class ExportFormatDialog(QDialog):
    """
    Diálogo para seleccionar el formato de exportación de log.
    """

    def __init__(self, log_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("export_log"))
        layout = QVBoxLayout(self)
        label = QLabel(translation_service.tr("select_export_format"))
        layout.addWidget(label)
        self.combo = QComboBox(self)
        # Usar Enum LogType para decidir los formatos
        if log_type == LogType.OPERATION_LOG:
            self.formats = [
                ("TXT", ".txt"),
                ("CSV", ".csv"),
                ("ADI", ".adi"),
            ]
        elif log_type == LogType.CONTEST_LOG:
            self.formats = [
                ("PDF", ".pdf"),
                ("CSV", ".csv"),
                ("ADI", ".adi"),
            ]
        else:
            raise ValueError(f"Tipo de log no soportado: {log_type}")
        self.combo.addItems([f[0] for f in self.formats])
        layout.addWidget(self.combo)
        btn_ok = QPushButton(translation_service.tr("ok_button"), self)
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)
        self.selected_ext = None

    def accept(self):
        """
        Obtiene la extensión seleccionada y cierra el diálogo.
        """
        idx = self.combo.currentIndex()
        self.selected_ext = self.formats[idx][1]
        super().accept()
