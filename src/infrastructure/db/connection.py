"""
connection.py

Módulo encargado de la gestión de conexiones a bases de datos SQLite.
Permite abrir conexiones tanto a la base principal como a bases auxiliares.
"""

import sqlite3
from typing import Optional


def get_connection(db_path: str) -> Optional[sqlite3.Connection]:
    """
    Abre una conexión a la base de datos SQLite especificada.
    Args:
        db_path (str): Ruta al archivo de la base de datos.
    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Error al conectar a la base de datos {db_path}: {e}")
