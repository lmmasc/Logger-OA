from enum import Enum
from PySide6.QtWidgets import QStackedWidget


class ViewID(Enum):
    WELCOME_VIEW = "welcome_view"
    LOG_OPS_VIEW = "log_ops_view"
    LOG_CONTEST_VIEW = "log_contest_view"
    # Agrega aquí otros identificadores de vistas según sea necesario


class LogType(Enum):
    OPERATION_LOG = "operation_log"
    CONTEST_LOG = "contest_log"


class ViewManager:
    """
    Gestor centralizado de vistas para la aplicación.
    Permite registrar, mostrar y acceder a vistas de forma desacoplada.
    """

    def __init__(self, parent=None):
        self.stacked_widget = QStackedWidget(parent)
        self.views = {}

    def register_view(self, view_id: ViewID, view_instance):
        """
        Registra una vista usando un identificador del Enum ViewID.
        """
        self.views[view_id] = view_instance
        self.stacked_widget.addWidget(view_instance)

    def show_view(self, view_id: ViewID):
        """
        Muestra la vista correspondiente al identificador ViewID.
        """
        if view_id in self.views:
            self.stacked_widget.setCurrentWidget(self.views[view_id])

    def get_widget(self):
        return self.stacked_widget
