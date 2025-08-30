"""
file_manager.py

Módulo para manejo de archivos y rutas en la aplicación Logger OA v2.
Incluye utilidades para obtener rutas, verificar existencia y crear carpetas.
"""

import os
from pathlib import Path


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
