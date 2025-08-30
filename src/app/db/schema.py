# db/schema.py


def init_radioamateur_table(conn):
    """
    Crea la tabla de radioaficionados si no existe.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS radioamateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        callsign TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        country TEXT NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
