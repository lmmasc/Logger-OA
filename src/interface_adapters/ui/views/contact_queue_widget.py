from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QMenu,
    QHBoxLayout,
    QListWidgetItem,
    QListView,
)
from translation.translation_service import translation_service


class ContactQueueWidget(QWidget):
    """
    Widget para mostrar la cola de contactos en espera de confirmación o revisión.
    """

    setCallsign = Signal(str)  # Señal para copiar al campo de indicativo

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.label = QLabel(translation_service.tr("contact_queue"), self)
        self.queue_list = QListWidget(self)
        self.queue_list.setFlow(QListView.LeftToRight)
        self.queue_list.setWrapping(False)
        self.label.setFixedHeight(42)
        self.queue_list.setFixedHeight(58)
        font = self.queue_list.font()
        font.setPointSize(18)
        self.queue_list.setFont(font)
        self.queue_list.setStyleSheet(
            "QListWidget::item { background: #1976d2; color: white; border-radius: 8px; margin: 2px 8px; padding: 2px 8px; min-width: 0px; font-weight: bold; min-height: 28px; max-height: 32px; } QListWidget::item:selected { background: #1565c0; }"
        )
        self.queue_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.queue_list)
        self.setLayout(self.layout)
        self.queue_list.setSelectionMode(QListWidget.SingleSelection)
        self.queue_list.itemClicked.connect(self._on_item_clicked)
        self.queue_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.queue_list.customContextMenuRequested.connect(self._on_context_menu)

    def set_queue(self, contacts):
        self.queue_list.clear()
        for contact in contacts:
            self.queue_list.addItem(str(contact))

    def add_to_queue(self, text):
        item = QListWidgetItem(text)
        self.queue_list.addItem(item)

    def remove_selected(self):
        item = self.queue_list.currentItem()
        if item:
            self.queue_list.takeItem(self.queue_list.row(item))

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("contact_queue"))

    def _on_item_clicked(self, item):
        self.setCallsign.emit(item.text())

    def _on_context_menu(self, pos):
        item = self.queue_list.itemAt(pos)
        if item:
            menu = QMenu(self)
            remove_action = menu.addAction("Eliminar")
            action = menu.exec(self.queue_list.mapToGlobal(pos))
            if action == remove_action:
                self.queue_list.takeItem(self.queue_list.row(item))
