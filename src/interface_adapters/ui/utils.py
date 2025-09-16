"""
Módulo de utilidades para la interfaz gráfica de usuario.

Contiene funciones auxiliares para la gestión de widgets en la aplicación Logger OA.
"""

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from interface_adapters.ui.main_window import MainWindow


def find_main_window(widget) -> "MainWindow | None":
    """
    Busca la instancia de la ventana principal (MainWindow) a partir de un widget hijo.

    Args:
        widget: Widget hijo desde el cual se inicia la búsqueda.

    Returns:
        MainWindow: Instancia de la ventana principal si se encuentra, de lo contrario None.

    Recorrido:
        Sube por la jerarquía de padres del widget hasta encontrar un objeto cuyo nombre de clase sea 'MainWindow'.
    """
    parent = widget.parent()
    while parent:
        if parent.__class__.__name__ == "MainWindow":
            return cast("MainWindow", parent)
        parent = parent.parent()
    return None
