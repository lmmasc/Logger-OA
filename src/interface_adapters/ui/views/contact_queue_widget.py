"""
ContactQueueWidget: Widget para mostrar y gestionar la cola de contactos en espera.
- Permite copiar indicativo, agregar, eliminar y traducir el label.
- Elimina el focus rectangle nativo en los items usando un delegate personalizado.
"""

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QListWidget,
    QLabel,
    QMenu,
    QListWidgetItem,
    QListView,
    QStyledItemDelegate,
    QStyle,
)
from translation.translation_service import translation_service


class NoFocusDelegate(QStyledItemDelegate):
    """
    Delegate personalizado para eliminar el focus rectangle nativo en los items de QListWidget.
    """

    def paint(self, painter, option, index):
        option.state &= ~QStyle.StateFlag.State_HasFocus
        super().paint(painter, option, index)


class ContactQueueWidget(QWidget):
    """
    Widget para mostrar la cola de contactos en espera de confirmación o revisión.
    Permite agregar, eliminar y copiar indicativos, y adapta el label al idioma.
    """

    setCallsign = Signal(str)

    def __init__(self, parent=None):
        """
        Inicializa el widget de cola de contactos.
        Args:
            parent (QWidget): Widget padre.
        """
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        self.label = QLabel(translation_service.tr("contact_queue"), self)
        self.queue_list = QListWidget(self)
        self.queue_list.setFlow(QListView.Flow.LeftToRight)
        self.queue_list.setWrapping(False)
        self.label.setFixedHeight(42)
        self.queue_list.setFixedHeight(68)
        font = self.queue_list.font()
        font.setPointSize(18)
        self.queue_list.setFont(font)
        self.queue_list.setObjectName("ContactQueueList")
        self.queue_list.setItemDelegate(NoFocusDelegate())
        self.queue_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.queue_list)
        self.setLayout(main_layout)
        self.queue_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.queue_list.itemClicked.connect(self._on_item_clicked)
        self.queue_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.queue_list.customContextMenuRequested.connect(self._on_context_menu)

    def set_queue(self, contacts):
        """
        Establece la lista completa de contactos en la cola.
        Args:
            contacts (list): Lista de contactos a mostrar.
        """
        self.queue_list.clear()
        for contact in contacts:
            self.queue_list.addItem(str(contact))

    def add_to_queue(self, text):
        """
        Agrega un contacto a la cola.
        Args:
            text (str): Texto del contacto a agregar.
        """
        item = QListWidgetItem(text)
        self.queue_list.addItem(item)

    def remove_selected(self):
        """
        Elimina el contacto seleccionado de la cola.
        """
        item = self.queue_list.currentItem()
        if item:
            self.queue_list.takeItem(self.queue_list.row(item))

    def retranslate_ui(self):
        """
        Actualiza el label según el idioma actual.
        """
        self.label.setText(translation_service.tr("contact_queue"))

    def _on_item_clicked(self, item):
        """
        Emite la señal setCallsign con el texto del contacto seleccionado.
        Args:
            item (QListWidgetItem): Item seleccionado.
        """
        self.setCallsign.emit(item.text())

    def _on_context_menu(self, pos):
        """
        Muestra menú contextual para eliminar el contacto seleccionado.
        Args:
            pos (QPoint): Posición del menú.
        """
        item = self.queue_list.itemAt(pos)
        if item:
            menu = QMenu(self)
            remove_action = menu.addAction("Eliminar")
            action = menu.exec(self.queue_list.mapToGlobal(pos))
            if action == remove_action:
                self.queue_list.takeItem(self.queue_list.row(item))
