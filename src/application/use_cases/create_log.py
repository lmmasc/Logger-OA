from datetime import datetime
from domain.entities.operation import OperationLog
from domain.entities.contest import ContestLog
from domain.repositories.contact_log_repository import ContactLogRepository
from config.paths import get_log_file_path
from interface_adapters.ui.view_manager import LogType


def create_log(log_type: LogType, operator_callsign: str, **kwargs):
    """
    Crea un nuevo log (operativo o concurso), genera el archivo SQLite y guarda el log inicial.
    log_type debe ser un Enum LogType.
    kwargs puede incluir campos adicionales según el tipo de log.
    """
    from datetime import timezone

    timestamp = int(datetime.now(timezone.utc).timestamp())
    # Extraer campos relevantes para el nombre de archivo
    if log_type == LogType.OPERATION_LOG:
        operation_type = kwargs.pop("operation_type", "type")
        frequency_band = kwargs.pop("frequency_band", "band")
        repeater_key = kwargs.pop("repeater_key", None)
        db_path = get_log_file_path(
            operator_callsign,
            log_type,
            timestamp,
            operation_type=operation_type,
            frequency_band=frequency_band,
            repeater_key=repeater_key,
        )
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
    elif log_type == LogType.CONTEST_LOG:
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
        raise ValueError(f"Tipo de log no soportado: {log_type}")

    log.db_path = db_path
    repo = ContactLogRepository(db_path)
    repo.save_log(log, log_type.value)
    return db_path, log
