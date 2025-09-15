import os
import json
import sqlite3
from domain.repositories.contact_log_repository import ContactLogRepository
from domain.entities.operation import OperationLog
from domain.entities.contest import ContestLog
from config.defaults import OPERATIONS_DIR, CONTESTS_DIR
from config.paths import BASE_PATH
from interface_adapters.ui.view_manager import LogType


def list_log_files(log_type: LogType) -> list:
    """
    Lista los archivos de logs disponibles para el tipo dado (LogType Enum).
    """
    if log_type == LogType.OPERATION_LOG:
        folder = os.path.join(BASE_PATH, OPERATIONS_DIR)
    elif log_type == LogType.CONTEST_LOG:
        folder = os.path.join(BASE_PATH, CONTESTS_DIR)
    else:
        raise ValueError(f"Tipo de log no soportado: {log_type}")
    if not os.path.exists(folder):
        return []
    return [
        os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".sqlite")
    ]


def open_log(db_path: str):
    """
    Abre y carga un log existente desde su archivo SQLite.
    Devuelve una instancia de OperationLog o ContestLog según corresponda.
    """
    repo = ContactLogRepository(db_path)
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, type, operator, start_time, end_time, metadata FROM logs LIMIT 1"
        )
        row = c.fetchone()
        if not row:
            raise FileNotFoundError("No se encontró ningún log en la base de datos.")
        log_type = row[1]
        metadata = json.loads(row[5]) if row[5] else {}
        if log_type == LogType.OPERATION_LOG.value:
            log = OperationLog(
                id=row[0],
                operator=row[2],
                start_time=row[3],
                end_time=row[4],
                metadata=metadata,
            )
            log.log_type = LogType.OPERATION_LOG
        elif log_type == LogType.CONTEST_LOG.value:
            log = ContestLog(
                id=row[0],
                operator=row[2],
                start_time=row[3],
                end_time=row[4],
                metadata=metadata,
            )
            log.log_type = LogType.CONTEST_LOG
        else:
            raise ValueError(f"Tipo de log no soportado: {log_type}")
    # Obtener contactos
    contacts = repo.get_contacts(log.id)
    log.contacts = contacts
    log.db_path = db_path
    return log
