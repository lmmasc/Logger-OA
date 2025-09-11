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


def normalize_filename_text(text):
    """
    Normaliza un texto para uso en nombres de archivo:
    - Convierte a minúsculas
    - Reemplaza espacios por '_'
    - Elimina caracteres especiales/accentos
    """
    import unicodedata

    text = text.lower().replace(" ", "_")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = "".join(c for c in text if c.isalnum() or c == "_")
    return text


def get_log_file_path(
    operator_callsign: str, log_type: str, timestamp: str, **kwargs
) -> str:
    """
    Genera el path absoluto para un archivo de log SQLite según el tipo (operativo/concurso),
    el indicativo del operador y el timestamp.
    El nombre de archivo usa los textos en español para tipo, banda y repetidora (si aplica), normalizados.
    Ejemplo: ~/LoggerOA/logs/oa4clu_cps_hf_r1_20250904t153000.sqlite
    """
    from .defaults import OPERATIONS_DIR, CONTESTS_DIR
    from translation.translation_service import translation_service

    log_type_folder = {"operativo": OPERATIONS_DIR, "concurso": CONTESTS_DIR}.get(
        log_type.lower(), "others"
    )
    folder = os.path.join(BASE_PATH, LOG_DIR, log_type_folder)
    os.makedirs(folder, exist_ok=True)
    # Nuevo formato de nombre de archivo
    if log_type.lower() == "operativo":
        operation_type_key = kwargs.get("operation_type", "type")
        frequency_band_key = kwargs.get("frequency_band", "band")
        repeater_key = kwargs.get("repeater_key")
        operation_type = translation_service.tr(operation_type_key)
        frequency_band = translation_service.tr(frequency_band_key)
        operation_type = normalize_filename_text(operation_type)
        frequency_band = normalize_filename_text(frequency_band)
        filename_parts = [operator_callsign.lower(), operation_type, frequency_band]
        if repeater_key:
            repeater = translation_service.tr(repeater_key)
            repeater = normalize_filename_text(repeater)
            filename_parts.append(repeater)
        filename_parts.append(timestamp.lower())
        filename = "_".join(filename_parts) + ".sqlite"
    elif log_type.lower() == "concurso":
        contest_key = kwargs.get("contest_key", "contest")
        contest_name = translation_service.tr(contest_key)
        contest_name = normalize_filename_text(contest_name)
        filename = (
            f"{operator_callsign.lower()}_{contest_name}_{timestamp.lower()}.sqlite"
        )
    else:
        filename = (
            f"{operator_callsign.lower()}_{log_type.lower()}_{timestamp.lower()}.sqlite"
        )
    print(
        "[DEBUG] get_log_file_path kwargs:",
        {
            "operation_type": operation_type_key,
            "frequency_band": frequency_band_key,
            "repeater_key": repeater_key,
        },
    )
    return os.path.join(folder, filename)
