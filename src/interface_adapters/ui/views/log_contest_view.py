from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from translation.translation_service import translation_service


class LogContestView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from .log_form_widget import LogFormWidget
        from .contact_table_widget import ContactTableWidget
        from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget

        layout = QVBoxLayout()
        self.label = QLabel(translation_service.tr("log_contest_title"))
        layout.addWidget(self.label)
        self.form_widget = LogFormWidget(self, log_type="contest")
        layout.addWidget(self.form_widget)
        self.suggestion_widget = CallsignSuggestionWidget(self)
        layout.addWidget(self.suggestion_widget)
        self.table_widget = ContactTableWidget(self, log_type="contest")
        layout.addWidget(self.table_widget)
        self.queue_widget = ContactQueueWidget(self)
        layout.addWidget(self.queue_widget)
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("log_contest_title"))
        self.form_widget.retranslate_ui()
        self.suggestion_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
