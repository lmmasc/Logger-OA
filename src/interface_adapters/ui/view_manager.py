from enum import Enum
from PySide6.QtWidgets import QStackedWidget


class ViewID(Enum):
    WELCOME_VIEW = "welcome_view"
    LOG_OPS_VIEW = "log_ops_view"
    LOG_CONTEST_VIEW = "log_contest_view"
    # Agrega aquí otros identificadores de vistas según sea necesario


class ViewManager:
    """
    Gestor centralizado de vistas para la aplicación.
    Permite registrar, mostrar y acceder a vistas de forma desacoplada.
    """

    def __init__(self, parent=None):
        self.stacked_widget = QStackedWidget(parent)
        self.views = {}

    def register_view(self, name, view_instance):
        self.views[name] = view_instance
        self.stacked_widget.addWidget(view_instance)

    def show_view(self, name):
        if name in self.views:
            self.stacked_widget.setCurrentWidget(self.views[name])

    def get_widget(self):
        return self.stacked_widget
