import os
import json
import sqlite3
from application.use_cases.log_file_format import (
    CURRENT_LOG_FILE_FORMAT_VERSION,
    normalize_contact,
    normalize_log_payload,
)
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
    file_format_version = repo.get_file_format_version()
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, type, operator, start_time, end_time, metadata FROM logs LIMIT 1"
        )
        row = c.fetchone()
        if not row:
            raise FileNotFoundError("No se encontró ningún log en la base de datos.")
        log_id = row[0]
        log_type = row[1]
        original_metadata = json.loads(row[5]) if row[5] else {}
        start_time, end_time, metadata = normalize_log_payload(
            log_type,
            row[3],
            row[4],
            original_metadata,
        )

        if log_type == LogType.OPERATION_LOG.value:
            log = OperationLog(
                id=log_id,
                operator=row[2],
                start_time=start_time,
                end_time=end_time,
                metadata=metadata,
            )
            log.log_type = LogType.OPERATION_LOG
        elif log_type == LogType.CONTEST_LOG.value:
            log = ContestLog(
                id=log_id,
                operator=row[2],
                start_time=start_time,
                end_time=end_time,
                metadata=metadata,
            )
            log.log_type = LogType.CONTEST_LOG
        else:
            raise ValueError(f"Tipo de log no soportado: {log_type}")

        header_needs_update = (
            row[3] != start_time
            or row[4] != end_time
            or metadata != original_metadata
            or file_format_version < CURRENT_LOG_FILE_FORMAT_VERSION
        )
        if header_needs_update:
            repo.save_log(log, log_type)
            repo.set_file_format_version(CURRENT_LOG_FILE_FORMAT_VERSION)
    # Obtener contactos
    contacts = repo.get_contacts(log.id)
    normalized_contacts = []
    for contact in contacts:
        normalized_contact = contact.copy() if isinstance(contact, dict) else contact
        if isinstance(normalized_contact, dict):
            migrated_contact = normalize_contact(log_type, normalized_contact)
            if migrated_contact != normalized_contact:
                repo.update_contact_data(migrated_contact["id"], migrated_contact)
            normalized_contact = migrated_contact
        normalized_contacts.append(normalized_contact)
    log.contacts = normalized_contacts
    log.db_path = db_path
    return log
