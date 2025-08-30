# db/schema.py


def init_radioamateur_table(conn):
    """
    Crea la tabla de radioaficionados si no existe.
    """
    sql = """
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
        cutoff_date TEXT,
        enabled INTEGER DEFAULT 1,
        country TEXT DEFAULT '',
        updated_at TEXT
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
