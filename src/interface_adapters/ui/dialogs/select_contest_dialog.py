from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class SelectContestDialog(QDialog):
    def __init__(self, parent=None):
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
        layout.addWidget(self.contest_box, alignment=Qt.AlignHCenter)
        self.ok_btn = QPushButton(translation_service.tr("ok_button"), self)
        self.ok_btn.setFixedWidth(200)
        layout.addWidget(self.ok_btn, alignment=Qt.AlignHCenter)
        self.selected_contest = None
        self.ok_btn.clicked.connect(self.set_contest)

    def set_contest(self):
        self.selected_contest = self.contest_box.currentText()
        self.accept()
