"""
paths.py

Funciones utilitarias para obtener rutas relevantes según el entorno.
"""

import os
from .defaults import DATA_FOLDER, EXPORT_FOLDER, LOG_FOLDER
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_data_path(filename=None):
    path = os.path.join(BASE_DIR, DATA_FOLDER)
    if filename:
        return os.path.join(path, filename)
    return path


def get_export_path(filename=None):
    path = os.path.join(BASE_DIR, EXPORT_FOLDER)
    if filename:
        return os.path.join(path, filename)
    return path


def get_log_path(filename=None):
    path = os.path.join(BASE_DIR, LOG_FOLDER)
    if filename:
        return os.path.join(path, filename)
    return path


def get_db_path(filename="loggeroa.db"):
    """
    Devuelve la ruta absoluta recomendada para la base de datos SQLite.
    Por defecto, la base se almacena en ~/LoggerOA/loggeroa.db
    """
    db_dir = Path.home() / "LoggerOA"
    db_dir.mkdir(exist_ok=True)
    return str(db_dir / filename)


def ensure_dir_exists(path):
    """
    Crea el directorio si no existe.
    """
    os.makedirs(path, exist_ok=True)


def file_exists(path):
    """
    Verifica si un archivo existe.
    """
    return Path(path).exists()
