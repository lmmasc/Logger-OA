import os
from domain.repositories.contact_log_repository import ContactLogRepository
from domain.entities.operation import OperationLog
from domain.entities.contest import ContestLog
import json


def list_log_files(log_type: str) -> list:
    """
    Lista los archivos de logs disponibles para el tipo dado (operativo/concurso).
    """
    from src.config.paths import BASE_DIR

    folder = os.path.join(
        BASE_DIR, "operativos" if log_type == "operativo" else "concursos"
    )
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
    with repo:
        # Obtener el log principal
        with repo._connect() as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, type, operator, start_time, end_time, metadata FROM logs LIMIT 1"
            )
            row = c.fetchone()
            if not row:
                raise FileNotFoundError(
                    "No se encontró ningún log en la base de datos."
                )
            log_type = row[1]
            metadata = json.loads(row[5]) if row[5] else {}
            if log_type == "OperationLog":
                log = OperationLog(
                    id=row[0],
                    operator=row[2],
                    start_time=row[3],
                    end_time=row[4],
                    metadata=metadata,
                )
            elif log_type == "ContestLog":
                log = ContestLog(
                    id=row[0],
                    operator=row[2],
                    start_time=row[3],
                    end_time=row[4],
                    metadata=metadata,
                )
            else:
                raise ValueError("Tipo de log no soportado")
        # Obtener contactos
        contacts = repo.get_contacts(log.id)
        log.contacts = contacts
    return log
