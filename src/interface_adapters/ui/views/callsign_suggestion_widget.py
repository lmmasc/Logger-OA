from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget
from translation.translation_service import translation_service


class CallsignSuggestionWidget(QWidget):
    """
    Widget para sugerencias/autocompletado de indicativos.
    """

    def __init__(self, parent=None, callsigns=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.input = QLineEdit(self)
        self.suggestion_list = QListWidget(self)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.suggestion_list)
        self.setLayout(self.layout)
        self.callsigns = callsigns or []
        self.input.textChanged.connect(self.update_suggestions)

    def update_suggestions(self, text):
        self.suggestion_list.clear()
        if not text:
            return
        filtered = [c for c in self.callsigns if text.upper() in c.upper()]
        self.suggestion_list.addItems(filtered)

    def set_callsigns(self, callsigns):
        self.callsigns = callsigns

    def retranslate_ui(self):
        self.input.setPlaceholderText(translation_service.tr("callsign"))
