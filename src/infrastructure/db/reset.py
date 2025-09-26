def reset_database():
    """
    Borra el archivo de la base de datos y crea una nueva base vacía.
    """
    import os
    from config.paths import get_database_path
    from .connection import get_connection
    from .schema import init_radioamateur_table

    db_path = get_database_path()
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = get_connection(db_path)
    if conn:
        init_radioamateur_table(conn)
        conn.close()


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
    # Solo borrar la tabla de operadores
    cursor.execute("DELETE FROM radio_operators;")
    conn.commit()
    cursor.execute("VACUUM;")
    conn.close()
