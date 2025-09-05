from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from translation.translation_service import translation_service


class LogContestView(QWidget):
    def __init__(self, parent=None, callsign="", log_type_name="Concurso", log_date=""):
        super().__init__(parent)
        from .log_form_widget import LogFormWidget
        from .contact_table_widget import ContactTableWidget
        from .callsign_suggestion_widget import CallsignSuggestionWidget
        from .contact_queue_widget import ContactQueueWidget

        layout = QVBoxLayout()
        # Encabezado dinámico
        header_text = f"{callsign} | {log_type_name} | {log_date}"
        self.header_label = QLabel(header_text)
        self.header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header_label)
        self.form_widget = LogFormWidget(self, log_type="contest")
        layout.addWidget(self.form_widget)
        self.suggestion_widget = CallsignSuggestionWidget(self)
        layout.addWidget(self.suggestion_widget)
        self.queue_widget = ContactQueueWidget(self)
        layout.addWidget(self.queue_widget)
        self.table_widget = ContactTableWidget(self, log_type="contest")
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        translation_service.signal.language_changed.connect(self.retranslate_ui)

    def retranslate_ui(self):
        # El encabezado se mantiene parametrizable, puedes actualizarlo aquí si cambian los datos
        self.form_widget.retranslate_ui()
        self.suggestion_widget.retranslate_ui()
        self.table_widget.retranslate_ui()
        self.queue_widget.retranslate_ui()
