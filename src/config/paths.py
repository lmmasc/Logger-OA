"""
paths.py

Funciones utilitarias para obtener rutas relevantes según el entorno.
"""

import os
from .defaults import DATA_DIR, EXPORT_DIR, LOG_DIR
from pathlib import Path

# BASE_PATH apunta a la carpeta de usuario (~) para almacenar archivos generados por la app
BASE_PATH = str(Path.home() / "LoggerOA")
os.makedirs(BASE_PATH, exist_ok=True)


def get_data_dir(filename=None):
    path = os.path.join(BASE_PATH, DATA_DIR)
    os.makedirs(path, exist_ok=True)
    if filename:
        return os.path.join(path, filename)
    return path


def get_export_dir(filename=None):
    path = os.path.join(BASE_PATH, EXPORT_DIR)
    os.makedirs(path, exist_ok=True)
    if filename:
        return os.path.join(path, filename)
    return path


def get_log_dir(filename=None):
    path = os.path.join(BASE_PATH, LOG_DIR)
    os.makedirs(path, exist_ok=True)
    if filename:
        return os.path.join(path, filename)
    return path


def get_database_path(filename="loggeroa.db"):
    """
    Devuelve la ruta absoluta recomendada para la base de datos SQLite.
    Por defecto, la base se almacena en ~/LoggerOA/loggeroa.db
    """
    db_dir = Path(BASE_PATH)
    db_dir.mkdir(exist_ok=True)
    return str(db_dir / filename)


def ensure_directory_exists(path):
    """
    Crea el directorio si no existe.
    """
    os.makedirs(path, exist_ok=True)


def file_exists(path):
    """
    Verifica si un archivo existe.
    """
    return Path(path).exists()


def get_log_file_path(
    operator_callsign: str, log_type: str, timestamp: str, **kwargs
) -> str:
    """
    Genera el path absoluto para un archivo de log SQLite según el tipo (operativo/concurso),
    el indicativo del operador y el timestamp.
    Ejemplo: ~/LoggerOA/logs/LU1ABC_operation_20250904T153000.sqlite
    """
    log_type_folder = {"operativo": "operations", "concurso": "contests"}.get(
        log_type.lower(), "others"
    )
    folder = os.path.join(BASE_PATH, LOG_DIR, log_type_folder)
    os.makedirs(folder, exist_ok=True)
    # Nuevo formato de nombre de archivo
    if log_type.lower() == "operativo":
        operation_type = kwargs.get("tipo", "type")
        band = kwargs.get("banda", "band")
        filename = f"{operator_callsign}_{operation_type}_{band}_{timestamp}.sqlite"
    elif log_type.lower() == "concurso":
        contest_name = kwargs.get("concurso", "contest")
        filename = f"{operator_callsign}_{contest_name}_{timestamp}.sqlite"
    else:
        filename = f"{operator_callsign}_{log_type}_{timestamp}.sqlite"
    return os.path.join(folder, filename)
