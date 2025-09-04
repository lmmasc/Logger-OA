from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel
from translation.translation_service import translation_service


class ContactQueueWidget(QWidget):
    """
    Widget para mostrar la cola de contactos en espera de confirmación o revisión.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(translation_service.tr("contact_queue"), self)
        self.queue_list = QListWidget(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.queue_list)
        self.setLayout(self.layout)

    def set_queue(self, contacts):
        self.queue_list.clear()
        for contact in contacts:
            self.queue_list.addItem(str(contact))

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("contact_queue"))
