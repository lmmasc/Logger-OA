"""
queries.py

Módulo con funciones para operaciones CRUD y consultas sobre bases de datos SQLite.
Permite trabajar tanto con la base principal como con bases auxiliares.
"""

from typing import Any, List, Tuple, Optional
from .connection import get_connection
from config.paths import get_database_path


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
        raise RuntimeError(f"Error ejecutando query: {e}")
    finally:
        conn.close()


def add_radio_operator(
    callsign,
    name,
    category,
    type_,
    region,
    district,
    province,
    department,
    license_,
    resolution,
    expiration_date,
    cutoff_date,
    enabled,
    country,
    updated_at,
):
    """
    Inserta un nuevo operador de radio.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    sql = (
        "INSERT INTO radio_operators (callsign, name, category, type, region, district, province, department, "
        "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    cursor = conn.cursor()
    cursor.execute(
        sql,
        (
            callsign,
            name,
            category,
            type_,
            region,
            district,
            province,
            department,
            license_,
            resolution,
            expiration_date,
            cutoff_date,
            enabled,
            country,
            updated_at,
        ),
    )
    conn.commit()
    conn.close()


def get_radio_operators():
    """
    Devuelve todos los operadores de radio.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    sql = (
        "SELECT callsign, name, category, type, region, district, province, department, "
        "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at "
        "FROM radio_operators"
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def update_radio_operator(
    callsign,
    name,
    category,
    type_,
    region,
    district,
    province,
    department,
    license_,
    resolution,
    expiration_date,
    cutoff_date,
    enabled,
    country,
    updated_at,
):
    """
    Actualiza un operador de radio por callsign.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    sql = (
        "UPDATE radio_operators SET name=?, category=?, type=?, region=?, district=?, province=?, department=?, "
        "license=?, resolution=?, expiration_date=?, cutoff_date=?, enabled=?, country=?, updated_at=? "
        "WHERE callsign=?"
    )
    cursor = conn.cursor()
    cursor.execute(
        sql,
        (
            name,
            category,
            type_,
            region,
            district,
            province,
            department,
            license_,
            resolution,
            expiration_date,
            cutoff_date,
            enabled,
            country,
            updated_at,
            callsign,
        ),
    )
    conn.commit()
    conn.close()


def delete_radio_operator(callsign):
    """
    Elimina un operador de radio por callsign.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    sql = "DELETE FROM radio_operators WHERE callsign=?"
    cursor = conn.cursor()
    cursor.execute(sql, (callsign,))
    conn.commit()
    conn.close()


def delete_radio_operator_by_callsign(callsign):
    """
    Elimina un operador de radio por callsign (alias para compatibilidad con repositorio).
    """
    return delete_radio_operator(callsign)


def get_radio_operator_by_callsign(callsign: str):
    """
    Devuelve el operador de radio con el indicativo exacto.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    sql = (
        "SELECT callsign, name, category, type, region, district, province, department, "
        "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at "
        "FROM radio_operators WHERE callsign = ?"
    )
    cursor = conn.cursor()
    cursor.execute(sql, (callsign,))
    result = cursor.fetchone()
    conn.close()
    return result
