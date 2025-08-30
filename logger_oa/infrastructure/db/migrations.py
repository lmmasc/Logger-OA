from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def apply_base_schema(conn: sqlite3.Connection) -> None:
    # Load schema.sql located alongside this file
    base = Path(__file__).resolve().parent
    schema_path = base / "schema.sql"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    else:
        # If schema file missing, create minimal required tables
        conn.executescript(
            """
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
        )
    # Ensure schema_version meta exists
    conn.execute(
        "INSERT OR IGNORE INTO meta (key, value) VALUES (?, ?)", ("schema_version", "1")
    )


__all__ = ["apply_base_schema"]
