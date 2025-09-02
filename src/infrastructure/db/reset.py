def reset_database():
    """
    Borra el archivo de la base de datos y crea una nueva base vacía.
    """
    import os
    from config.paths import get_db_path
    from .connection import get_connection
    from .schema import init_radioamateur_table

    db_path = get_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = get_connection(db_path)
    if conn:
        init_radioamateur_table(conn)
        conn.close()
