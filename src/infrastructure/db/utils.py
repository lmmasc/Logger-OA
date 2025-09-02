from pathlib import Path
import os


def get_db_path(filename="loggeroa.db"):
    """
    Devuelve la ruta absoluta recomendada para la base de datos SQLite.
    Por defecto, la base se almacena en ~/LoggerOA/loggeroa.db
    """
    db_dir = Path.home() / "LoggerOA"
    db_dir.mkdir(exist_ok=True)
    return str(db_dir / filename)
