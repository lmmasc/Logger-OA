"""
queries.py

Módulo con funciones para operaciones CRUD y consultas sobre bases de datos SQLite.
Permite trabajar tanto con la base principal como con bases auxiliares.
"""

from typing import Any, List, Tuple, Optional
from .connection import get_connection
from app.utils.file_manager import get_db_path


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


def add_radioamateur(callsign, name, country):
    """
    Inserta un nuevo radioaficionado.
    """
    db_path = get_db_path()
    conn = get_connection(db_path)
    sql = "INSERT INTO radioamateurs (callsign, name, country) VALUES (?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (callsign, name, country))
    conn.commit()
    conn.close()


def get_radioamateurs():
    """
    Devuelve todos los radioaficionados.
    """
    db_path = get_db_path()
    conn = get_connection(db_path)
    sql = "SELECT id, callsign, name, country FROM radioamateurs"
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def update_radioamateur(id, callsign, name, country):
    """
    Actualiza un radioaficionado por id.
    """
    db_path = get_db_path()
    conn = get_connection(db_path)
    sql = "UPDATE radioamateurs SET callsign=?, name=?, country=? WHERE id=?"
    cursor = conn.cursor()
    cursor.execute(sql, (callsign, name, country, id))
    conn.commit()
    conn.close()


def delete_radioamateur(id):
    """
    Elimina un radioaficionado por id.
    """
    db_path = get_db_path()
    conn = get_connection(db_path)
    sql = "DELETE FROM radioamateurs WHERE id=?"
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()
    conn.close()
