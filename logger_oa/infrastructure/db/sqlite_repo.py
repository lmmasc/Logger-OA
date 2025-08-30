from __future__ import annotations

import sqlite3
from typing import Iterable, List, Optional

from ...application.repositories.radio_operators import IRadioOperatorsRepo
from ...application.repositories.meta import IMetaRepo
from ...domain.models import RadioOperator
from ...utils.paths import get_database_path
from .migrations import apply_base_schema


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS radio_operators (
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
    enabled INTEGER,
    country TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""


UPSERT_SQL = """
    INSERT INTO radio_operators (
        callsign, name, category, type, district, province, department,
        license, resolution, expiration_date, enabled, country, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        enabled=excluded.enabled,
        country=excluded.country,
        updated_at=excluded.updated_at
    """


def _row_to_radio_operator(row: sqlite3.Row) -> RadioOperator:
    return RadioOperator(
        callsign=row["callsign"],
        name=row["name"] or "",
        category=row["category"] or "",
        type=row["type"] or "",
        district=row["district"] or "",
        province=row["province"] or "",
        department=row["department"] or "",
        license=row["license"] or "",
        resolution=row["resolution"] or "",
        expiration_date=row["expiration_date"] or "",
        enabled=int(row["enabled"]) if row["enabled"] is not None else 1,
        country=row["country"] or "",
        updated_at=row["updated_at"] or "",
    )


class _Conn:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or get_database_path()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


class SqliteRadioOperatorsRepo(IRadioOperatorsRepo):
    def __init__(self, db_path: Optional[str] = None):
        self._conn_helper = _Conn(db_path)

    def init_schema(self) -> None:
        with self._conn_helper.connect() as conn:
            try:
                apply_base_schema(conn)
            except Exception:
                # Fallback to inline schema if migrations helper fails
                conn.executescript(SCHEMA)
                conn.execute(
                    "INSERT OR IGNORE INTO meta (key, value) VALUES (?, ?)",
                    ("schema_version", "1"),
                )
            conn.commit()

    def upsert_many(self, items: Iterable[RadioOperator]) -> None:
        with self._conn_helper.connect() as conn:
            cur = conn.cursor()
            for it in items:
                cur.execute(
                    UPSERT_SQL,
                    (
                        it.callsign,
                        it.name,
                        it.category,
                        it.type,
                        it.district,
                        it.province,
                        it.department,
                        it.license,
                        it.resolution,
                        it.expiration_date,
                        it.enabled,
                        it.country,
                        it.updated_at,
                    ),
                )
            conn.commit()

    def upsert_one(self, item: RadioOperator) -> None:
        self.upsert_many([item])

    def list_all(self) -> List[RadioOperator]:
        with self._conn_helper.connect() as conn:
            cur = conn.execute(
                "SELECT * FROM radio_operators ORDER BY callsign COLLATE NOCASE"
            )
            return [_row_to_radio_operator(r) for r in cur.fetchall()]

    def delete_by_callsign(self, callsign: str) -> None:
        with self._conn_helper.connect() as conn:
            conn.execute("DELETE FROM radio_operators WHERE callsign = ?", (callsign,))
            conn.commit()

    def disable_by_callsign(self, callsign: str) -> None:
        with self._conn_helper.connect() as conn:
            conn.execute(
                "UPDATE radio_operators SET enabled = 0 WHERE callsign = ?",
                (callsign,),
            )
            conn.commit()


class SqliteMetaRepo(IMetaRepo):
    def __init__(self, db_path: Optional[str] = None):
        self._conn_helper = _Conn(db_path)

    def set(self, key: str, value: str) -> None:
        with self._conn_helper.connect() as conn:
            conn.execute("REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))
            conn.commit()

    def get(self, key: str) -> Optional[str]:
        with self._conn_helper.connect() as conn:
            cur = conn.execute("SELECT value FROM meta WHERE key = ?", (key,))
            row = cur.fetchone()
            return row["value"] if row else None


__all__ = [
    "SqliteRadioOperatorsRepo",
    "SqliteMetaRepo",
]
