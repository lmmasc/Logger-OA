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
