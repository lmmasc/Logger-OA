"""
Funciones para integrar los datos normalizados a la base de datos.
"""

import sqlite3
from datetime import datetime
from app.utils.file_manager import get_db_path


def integrate_operators_to_db(operators):
    """
    Inserta o actualiza los operadores en la base de datos SQLite local.
    Usa UPSERT para evitar duplicados y mantener actualizados los datos.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Crear tabla si no existe
    cur.execute(
        """CREATE TABLE IF NOT EXISTS radio_operators (
            callsign TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            type TEXT,
            district TEXT,
            province TEXT,
            department TEXT,
            license TEXT,
            resolution TEXT,
            expiration_date TEXT,
            cutoff_date TEXT,
            enabled INTEGER DEFAULT 1,
            country TEXT DEFAULT '',
            updated_at TEXT
        )"""
    )
    upsert_sql = """
            INSERT INTO radio_operators (
                callsign, name, category, type, district, province, department,
                license, resolution, expiration_date, cutoff_date, enabled, country, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(callsign) DO UPDATE SET
                name=excluded.name,
                category=excluded.category,
                type=excluded.type,
                district=excluded.district,
                province=excluded.province,
                department=excluded.department,
                license=excluded.license,
                resolution=excluded.resolution,
                expiration_date=excluded.expiration_date,
                cutoff_date=excluded.cutoff_date,
                enabled=excluded.enabled,
                country=excluded.country,
                updated_at=excluded.updated_at
        """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for op in operators:
        cur.execute(
            upsert_sql,
            (
                op["callsign"],
                op["name"],
                op["category"],
                op["type"],
                op["district"],
                op["province"],
                op["department"],
                op["license"],
                op["resolution"],
                op["expiration_date"],
                op.get("cutoff_date", ""),
                op.get("enabled", 1),
                op.get("country", ""),
                now,
            ),
        )
    conn.commit()
    conn.close()
    return True
