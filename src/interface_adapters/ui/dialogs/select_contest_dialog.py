"""
SelectContestDialog
Diálogo para seleccionar el concurso al crear un log de concurso.
"""

# --- Imports de terceros ---
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt

# --- Imports de la aplicación ---
from translation.translation_service import translation_service


class SelectContestDialog(QDialog):
    """
    Diálogo para seleccionar el concurso al crear un log de concurso.
    Permite elegir entre los concursos disponibles.
    """

    def __init__(self, parent=None):
        """
        Inicializa el diálogo de selección de concurso.
        Args:
            parent (QWidget, opcional): Widget padre.
        """
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("select_contest_title"))
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        label = QLabel(translation_service.tr("select_contest_label"))
        layout.addWidget(label)
        self.contest_box = QComboBox(self)
        self.contest_options = [
            translation_service.tr("contest_world_radio_day"),
            translation_service.tr("contest_independence_peru"),
            translation_service.tr("contest_peruvian_ham_day"),
        ]
        self.contest_box.addItems(self.contest_options)
        layout.addWidget(self.contest_box, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.ok_btn = QPushButton(translation_service.tr("ok_button"), self)
        self.ok_btn.setFixedWidth(200)
        layout.addWidget(self.ok_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.selected_contest = None
        self.ok_btn.clicked.connect(self.set_contest)

    def set_contest(self):
        """
        Establece el concurso seleccionado y cierra el diálogo.
        """
        self.selected_contest = self.contest_box.currentText()
        self.accept()
