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
    _ensure_indexes(conn)
    sql = (
        "SELECT callsign, name, category, type, region, district, province, department, "
        "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at "
        "FROM radio_operators ORDER BY callsign ASC"
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
    _ensure_indexes(conn)
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


def search_radio_operators_by_callsign(pattern: str, limit: int = 50):
    """
    Busca operadores por callsign usando LIKE, devolviendo solo callsign y name.
    pattern: patrón con % y _ (comodines SQL). Se aplica COLLATE NOCASE.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    _ensure_indexes(conn)
    sql = (
        "SELECT callsign, name FROM radio_operators "
        "WHERE callsign LIKE ? ESCAPE '\\' COLLATE NOCASE "
        "ORDER BY LENGTH(callsign) ASC, callsign ASC LIMIT ?"
    )
    cursor = conn.cursor()
    cursor.execute(sql, (pattern, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows


def _ensure_indexes(conn):
    """
    Crea índices necesarios si no existen para acelerar búsquedas y ORDER BY.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_radio_operators_callsign ON radio_operators(callsign)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_radio_operators_country ON radio_operators(country)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_radio_operators_enabled ON radio_operators(enabled)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_radio_operators_name ON radio_operators(name)"
        )
        conn.commit()
    except Exception:
        pass


def _build_filter_clause(filter_col: Optional[str], filter_text: Optional[str]):
    if filter_col and filter_text:
        # LIKE con comodines en ambas puntas, case-insensitive
        return f" WHERE {filter_col} LIKE ? COLLATE NOCASE ", f"%{filter_text}%"
    return "", None


def get_radio_operators_paged(
    page: int,
    page_size: int,
    order_by: str = "callsign",
    asc: bool = True,
    filter_col: Optional[str] = None,
    filter_text: Optional[str] = None,
) -> Tuple[List[Tuple], int]:
    """
    Devuelve filas paginadas y el total, con filtro opcional por columna usando LIKE.
    """
    db_path = get_database_path()
    conn = get_connection(db_path)
    _ensure_indexes(conn)
    order = "ASC" if asc else "DESC"
    where_clause, where_param = _build_filter_clause(filter_col, filter_text)
    base_select = (
        "SELECT callsign, name, category, type, region, district, province, department, "
        "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at "
        f"FROM radio_operators{where_clause} ORDER BY {order_by} {order} LIMIT ? OFFSET ?"
    )
    base_count = f"SELECT COUNT(*) FROM radio_operators{where_clause}"
    cur = conn.cursor()
    params = []
    if where_param is not None:
        params.append(where_param)
    params.extend([page_size, page * page_size])
    cur.execute(base_select, tuple(params))
    rows = cur.fetchall()
    count_params = []
    if where_param is not None:
        count_params.append(where_param)
    cur.execute(base_count, tuple(count_params))
    total = cur.fetchone()[0]
    conn.close()
    return rows, int(total)


def disable_expired_operators() -> int:
    """
    Deshabilita TODOS los operadores con expiration_date vencida, independientemente del país.
    Retorna la cantidad de filas afectadas.

    Si un operador no tiene expiration_date, permanece habilitado.
    Solo se deshabilitan los que tienen fecha válida y ya vencida.
    """
    from datetime import datetime, timezone

    now_ts = int(datetime.now(timezone.utc).timestamp())
    db_path = get_database_path()
    conn = get_connection(db_path)
    try:
        cur = conn.cursor()
        # Actualizar enabled=0 solo cuando está actualmente en 1, la fecha existe (no vacía)
        # y ya venció. Se castea expiration_date a INTEGER para bases donde está guardado como TEXT.
        sql = (
            f"UPDATE radio_operators "
            f"SET enabled = 0, updated_at = ? "
            f"WHERE IFNULL(enabled,1) = 1 "
            f"AND expiration_date IS NOT NULL "
            f"AND TRIM(expiration_date) <> '' "
            f"AND CAST(expiration_date AS INTEGER) > 0 "
            f"AND CAST(expiration_date AS INTEGER) < ?"
        )
        params = [now_ts, now_ts]
        cur.execute(sql, tuple(params))
        affected = cur.rowcount or 0
        conn.commit()
        return int(affected)
    finally:
        conn.close()


def disable_expired_for_countries(countries: Tuple[str, ...]) -> int:
    """
    DEPRECATED: Usar disable_expired_operators() en su lugar.
    Deshabilita operadores con expiration_date vencida para los países indicados.
    Mantenida por compatibilidad temporal.
    """
    # Por compatibilidad, simplemente llamar a la nueva función generalizada
    return disable_expired_operators()
