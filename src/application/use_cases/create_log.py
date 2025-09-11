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
    # Extraer campos relevantes para el nombre del archivo
    if log_type.lower() == "operativo":
        operation_type = kwargs.pop("operation_type", "type")
        frequency_band = kwargs.pop("frequency_band", "band")
        db_path = get_log_file_path(
            operator_callsign,
            log_type,
            timestamp,
            operation_type=operation_type,
            frequency_band=frequency_band,
        )
        # Mapear los campos del config dialog a los esperados por OperationLog
        log = OperationLog(
            operator=operator_callsign,
            start_time=timestamp,
            type=operation_type,
            band=frequency_band,
            mode=kwargs.get("mode_key", ""),
            frequency=kwargs.get("frequency", ""),
            repeater=kwargs.get("repeater_key", ""),
            metadata=kwargs.get("metadata", {}),
        )
    elif log_type.lower() == "concurso":
        contest_key = kwargs.pop("contest_key", "contest")
        db_path = get_log_file_path(
            operator_callsign, log_type, timestamp, contest_key=contest_key
        )
        log = ContestLog(
            operator=operator_callsign,
            start_time=timestamp,
            name=kwargs.get("name", contest_key),
            metadata=kwargs.get("metadata", {}),
        )
    else:
        db_path = get_log_file_path(operator_callsign, log_type, timestamp)
        raise ValueError("Tipo de log no soportado")

    log.db_path = db_path
    repo = ContactLogRepository(db_path)
    repo.save_log(log)
    return db_path, log
