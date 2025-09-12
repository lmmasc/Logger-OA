"""
backup_restore.py

Funciones para crear y restaurar backups de la base de datos de operadores.
"""

import os
import shutil
from datetime import datetime
from config.paths import get_database_path, BASE_PATH

BACKUP_DIR = os.path.join(BASE_PATH, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)


def create_backup():
    """
    Crea un backup del archivo de base de datos actual en la carpeta de backups.
    El nombre incluye fecha y hora para evitar sobrescritura.
    """
    src_db = get_database_path()
    if not os.path.exists(src_db):
        raise FileNotFoundError(f"No se encontró la base de datos: {src_db}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"loggeroa_backup_{timestamp}.db"
    dst_db = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(src_db, dst_db)
    return dst_db


def list_backups():
    """
    Lista los archivos de backup disponibles en la carpeta de backups.
    """
    return [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]


def restore_backup(backup_filename):
    """
    Restaura la base de datos desde un archivo de backup seleccionado.
    """
    src_backup = os.path.join(BACKUP_DIR, backup_filename)
    dst_db = get_database_path()
    if not os.path.exists(src_backup):
        raise FileNotFoundError(f"No se encontró el backup: {src_backup}")
    shutil.copy2(src_backup, dst_db)
    return dst_db


def import_from_external_db(external_db_path):
    """
    Importa operadores desde otra base de datos SQLite externa, evitando duplicados por callsign.
    """
    from infrastructure.db.queries import fetch_all, add_radio_operator

    # Leer operadores externos
    sql = (
        "SELECT callsign, name, category, type, region, district, province, department, "
        "license, resolution, expiration_date, cutoff_date, enabled, country, updated_at FROM radio_operators"
    )
    external_ops = fetch_all(external_db_path, sql)
    # Leer callsigns actuales
    current_ops = fetch_all(get_database_path(), sql)
    current_callsigns = set(row[0] for row in current_ops)
    # Importar solo nuevos
    imported = 0
    for row in external_ops:
        if row[0] not in current_callsigns:
            add_radio_operator(*row)
            imported += 1
    return imported
