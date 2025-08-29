"""
queries.py

Módulo con funciones para operaciones CRUD y consultas sobre bases de datos SQLite.
Permite trabajar tanto con la base principal como con bases auxiliares.
"""

from typing import Any, List, Tuple, Optional
from .connection import get_connection


def fetch_all(db_path: str, query: str, params: Tuple = ()) -> List[Tuple]:
    """
    Ejecuta una consulta SELECT y retorna todos los resultados.
    Args:
        db_path (str): Ruta a la base de datos.
        query (str): Consulta SQL SELECT.
        params (Tuple): Parámetros para la consulta.
    Returns:
        List[Tuple]: Lista de filas resultado.
    """
    conn = get_connection(db_path)
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    finally:
        conn.close()


def execute_query(db_path: str, query: str, params: Tuple = ()) -> bool:
    """
    Ejecuta una consulta INSERT, UPDATE o DELETE.
    Args:
        db_path (str): Ruta a la base de datos.
        query (str): Consulta SQL.
        params (Tuple): Parámetros para la consulta.
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario.
    """
    conn = get_connection(db_path)
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        return False
    finally:
        conn.close()
