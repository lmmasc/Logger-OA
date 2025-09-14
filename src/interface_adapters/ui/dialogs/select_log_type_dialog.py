from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
from interface_adapters.ui.view_manager import LogType


class SelectLogTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("select_log_type"))
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        label = QLabel(translation_service.tr("select_log_type_label_create"))
        layout.addWidget(label)
        self.btn_ops = QPushButton(translation_service.tr("log_type_ops"), self)
        self.btn_contest = QPushButton(translation_service.tr("log_type_contest"), self)
        self.btn_ops.setFixedWidth(200)
        self.btn_contest.setFixedWidth(200)
        layout.addWidget(self.btn_ops, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn_contest, alignment=Qt.AlignHCenter)
        self.selected_type = None
        self.btn_ops.clicked.connect(self.select_ops)
        self.btn_contest.clicked.connect(self.select_contest)

    def select_ops(self):
        self.selected_type = LogType.OPERATION_LOG
        self.accept()

    def select_contest(self):
        self.selected_type = LogType.CONTEST_LOG
        self.accept()
