import sys
import os


def get_resource_path(relative_path):
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller y desarrollo.
    """
    # sys._MEIPASS es un atributo especial que solo existe en tiempo de ejecución con PyInstaller.
    # Pylance no lo reconoce en los stubs, pero es seguro usarlo aquí.
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)  # type: ignore[attr-defined]
    # En desarrollo, usar la raíz del proyecto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, relative_path)
