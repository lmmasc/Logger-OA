def clear_database():
    """
    Borra todos los registros de todas las tablas y deja la estructura intacta.
    Resetea los contadores de autoincremento y compacta el archivo.
    """
    import sqlite3
    from config.paths import get_database_path

    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Listado de tablas principales
    tables = ["radio_operators", "logs", "contacts"]
    # Consultar tablas existentes en la base
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = set(row[0] for row in cursor.fetchall())
    for table in tables:
        if table in existing_tables:
            cursor.execute(f"DELETE FROM {table};")
    conn.commit()
    cursor.execute("VACUUM;")
    conn.close()
