"""
Módulo de gestión de vistas para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""


def show_view(self, view_name: str) -> None:
    """
    Cambia la vista central según el nombre dado usando el gestor de vistas.
    Args:
        view_name (str): Nombre de la vista a mostrar.
    """
    self.view_manager.show_view(view_name)


# Si existen otros métodos relacionados con la navegación de vistas, agrégalos aquí.
