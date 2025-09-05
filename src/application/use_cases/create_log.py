from datetime import datetime
from domain.entities.operation import OperationLog
from domain.entities.contest import ContestLog
from domain.repositories.contact_log_repository import ContactLogRepository
from config.paths import get_log_file_path


def create_log(log_type: str, operator_callsign: str, **kwargs):
    """
    Crea un nuevo log (operativo o concurso), genera el archivo SQLite y guarda el log inicial.
    kwargs puede incluir campos adicionales según el tipo de log.
    """
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    db_path = get_log_file_path(operator_callsign, log_type, timestamp)
    repo = ContactLogRepository(db_path)

    if log_type.lower() == "operativo":
        log = OperationLog(operator=operator_callsign, start_time=timestamp, **kwargs)
    elif log_type.lower() == "concurso":
        log = ContestLog(operator=operator_callsign, start_time=timestamp, **kwargs)
    else:
        raise ValueError("Tipo de log no soportado")

    repo.save_log(log)
    return db_path, log
