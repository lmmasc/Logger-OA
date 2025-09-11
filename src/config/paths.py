"""
paths.py

Funciones utilitarias para obtener rutas relevantes según el entorno.
"""

import os
from .defaults import DATA_FOLDER, EXPORT_FOLDER, LOG_FOLDER
from pathlib import Path

# BASE_DIR apunta a la carpeta de usuario (~) para almacenar archivos generados por la app
BASE_DIR = str(Path.home() / "LoggerOA")
os.makedirs(BASE_DIR, exist_ok=True)


def get_data_path(filename=None):
    path = os.path.join(BASE_DIR, DATA_FOLDER)
    os.makedirs(path, exist_ok=True)
    if filename:
        return os.path.join(path, filename)
    return path


def get_export_path(filename=None):
    path = os.path.join(BASE_DIR, EXPORT_FOLDER)
    os.makedirs(path, exist_ok=True)
    if filename:
        return os.path.join(path, filename)
    return path


def get_log_path(filename=None):
    path = os.path.join(BASE_DIR, LOG_FOLDER)
    os.makedirs(path, exist_ok=True)
    if filename:
        return os.path.join(path, filename)
    return path


def get_db_path(filename="loggeroa.db"):
    """
    Devuelve la ruta absoluta recomendada para la base de datos SQLite.
    Por defecto, la base se almacena en ~/LoggerOA/loggeroa.db
    """
    db_dir = Path(BASE_DIR)
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


def get_log_file_path(
    operator_callsign: str, log_type: str, timestamp: str, **kwargs
) -> str:
    """
    Genera el path absoluto para un archivo de log SQLite según el tipo (operativo/concurso),
    el indicativo del operador y el timestamp.
    Ejemplo: ~/LoggerOA/logs/LU1ABC_operativo_20250904T153000.sqlite
    """
    log_type_folder = {"operativo": "operativos", "concurso": "concursos"}.get(
        log_type.lower(), "otros"
    )
    folder = os.path.join(BASE_DIR, LOG_FOLDER, log_type_folder)
    os.makedirs(folder, exist_ok=True)
    # Nuevo formato de nombre de archivo
    if log_type.lower() == "operativo":
        tipo = kwargs.get("tipo", "tipo")
        banda = kwargs.get("banda", "banda")
        filename = f"{operator_callsign}_{tipo}_{banda}_{timestamp}.sqlite"
    elif log_type.lower() == "concurso":
        concurso = kwargs.get("concurso", "concurso")
        filename = f"{operator_callsign}_{concurso}_{timestamp}.sqlite"
    else:
        filename = f"{operator_callsign}_{log_type}_{timestamp}.sqlite"
    return os.path.join(folder, filename)
