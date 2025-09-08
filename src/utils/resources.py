import sys
import os


def get_resource_path(relative_path):
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller y desarrollo.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), "..", relative_path)
