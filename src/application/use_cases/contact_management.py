from domain.repositories.contact_log_repository import ContactLogRepository
from domain.entities.operation_contact import OperationContact
from domain.entities.contest_contact import ContestContact
from domain.entities.contact_log import ContactLog
from domain.validators import LogValidator
from domain.contest_rules import ContestRules
from domain.operation_rules import OperationRules
from domain.contact_type import ContactType


def add_contact_to_log(
    db_path: str,
    log_id: str,
    contact_data: dict,
    contact_type: ContactType = ContactType.OPERATION,
):
    """
    Agrega un contacto a un log existente (operativo o concurso) con validaciones de dominio.
    contact_data: diccionario con los datos del contacto.
    contact_type: 'operativo' u 'concurso'.
    """
    repo = ContactLogRepository(db_path)
    # Cargar contactos existentes para validación
    contacts = repo.get_contacts(log_id)
    if contact_type == ContactType.OPERATION:
        contact = OperationContact(**contact_data)
    elif contact_type == ContactType.CONTEST:
        contact = ContestContact(**contact_data)
    else:
        raise ValueError("Tipo de contacto no soportado")
    # Validaciones genéricas
    errors = LogValidator.validate_contact(contact, contacts)
    # Validaciones específicas
    if contact_type == ContactType.OPERATION:
        errors += OperationRules.validate(contact, contacts)
    elif contact_type == ContactType.CONTEST:
        errors += ContestRules.validate(contact, contacts)
    if errors:
        raise ValueError("; ".join(errors))
    # Si todo es válido, guardar
    repo.save_contact(log_id, contact)
    return contact


def delete_contact_from_log(db_path: str, contact_id: str):
    """
    Elimina un contacto de un log por su id.
    """
    repo = ContactLogRepository(db_path)
    repo.delete_contact(contact_id)


def update_contact_in_log(
    db_path: str,
    log_id: str,
    contact_id: str,
    updated_data: dict,
    contact_type: ContactType = ContactType.OPERATION,
):
    """
    Actualiza un contacto existente en un log, validando antes de guardar.
    """
    repo = ContactLogRepository(db_path)
    contacts = repo.get_contacts(log_id)
    # Crear y validar el nuevo contacto actualizado
    if contact_type == ContactType.OPERATION:
        contact = OperationContact(**updated_data)
    elif contact_type == ContactType.CONTEST:
        contact = ContestContact(**updated_data)
    else:
        raise ValueError("Tipo de contacto no soportado")
    # Validaciones genéricas
    errors = LogValidator.validate_contact(contact, contacts)
    # Validaciones específicas
    if contact_type == ContactType.OPERATION:
        errors += OperationRules.validate(contact, contacts)
    elif contact_type == ContactType.CONTEST:
        errors += ContestRules.validate(contact, contacts)
    if errors:
        raise ValueError("; ".join(errors))
    # Si todo es válido, actualizar el registro directamente
    repo.update_contact(contact_id, contact)
    return contact


def validate_contact_for_log(
    contact_data: dict, contacts: list, contact_type: ContactType, translation_service
) -> dict:
    """
    Valida el contacto, traduce y ordena los errores según el tipo de log y el orden visual del formulario.
    Devuelve dict con 'errors' (lista de mensajes) y 'focus_field' (str).
    """
    if contact_type == ContactType.OPERATION:
        contact = OperationContact(**contact_data)
    elif contact_type == ContactType.CONTEST:
        contact = ContestContact(**contact_data)
    else:
        return {
            "errors": [translation_service.tr("Tipo de contacto no soportado")],
            "focus_field": None,
        }
    errors = LogValidator.validate_contact(contact, contacts)
    if contact_type == ContactType.OPERATION:
        errors += OperationRules.validate(contact, contacts)
    elif contact_type == ContactType.CONTEST:
        errors += ContestRules.validate(contact, contacts)
    # Mapear errores a campos y traducir
    error_map = {}
    for err in errors:
        err = err.strip()
        if err == "Missing received exchange.":
            error_map["exchange_received_input"] = translation_service.tr(
                "validation_missing_received_exchange"
            )
        elif err == "Missing sent exchange.":
            error_map["exchange_sent_input"] = translation_service.tr(
                "validation_missing_sent_exchange"
            )
        elif err.startswith("Duplicate contact"):
            error_map["callsign_input"] = translation_service.tr(
                "validation_duplicate_contact"
            )
        elif err.startswith("Invalid callsign"):
            callsign = err.split(":", 1)[-1].strip()
            error_map["callsign_input"] = translation_service.tr(
                "validation_invalid_callsign"
            ).format(callsign=callsign)
        elif err.startswith("Invalid time format"):
            time = err.split(":", 1)[-1].strip()
            error_map["time_input"] = translation_service.tr(
                "validation_invalid_time_format"
            ).format(time=time)
        elif err == "Missing station.":
            error_map["station_input"] = translation_service.tr(
                "validation_missing_station"
            )
        elif err == "Missing power.":
            error_map["power_input"] = translation_service.tr(
                "validation_missing_power"
            )
        elif err.startswith("Invalid power value"):
            power = err.split(":", 1)[-1].strip()
            error_map["power_input"] = translation_service.tr(
                "validation_invalid_power_value"
            ).format(power=power)
        elif err == "Missing RS_RX.":
            error_map["rs_rx_input"] = translation_service.tr(
                "validation_missing_rs_rx"
            )
        elif err == "Missing RS_TX.":
            error_map["rs_tx_input"] = translation_service.tr(
                "validation_missing_rs_tx"
            )
        else:
            error_map["other"] = err
    # Orden de campos visuales
    if contact_type == ContactType.CONTEST:
        field_order = [
            "callsign_input",
            "rs_rx_input",
            "exchange_received_input",
            "rs_tx_input",
            "exchange_sent_input",
            "observations_input",
        ]
    else:
        field_order = [
            "callsign_input",
            "station_input",
            "energy_input",
            "power_input",
            "rs_rx_input",
            "rs_tx_input",
            "observations_input",
        ]
    translated_errors = []
    focus_field = None
    for field in field_order:
        if field in error_map:
            translated_errors.append(error_map[field])
            if focus_field is None:
                focus_field = field
    if "other" in error_map:
        translated_errors.append(error_map["other"])
    return {"errors": translated_errors, "focus_field": focus_field}


def get_oa_block_from_utc(timestamp_utc):
    """
    Calcula el bloque horario OA (1 o 2) a partir de un timestamp UTC.
    Retorna (bloque, hora_oa_str)
    """
    import datetime

    dt_utc = datetime.datetime.utcfromtimestamp(timestamp_utc)
    dt_oa = dt_utc - datetime.timedelta(hours=5)
    minute = dt_oa.minute
    block = 1 if 0 <= minute < 30 else 2
    hora_oa_str = dt_oa.strftime("%H:%M")
    return block, hora_oa_str


def find_duplicate_in_block(callsign, timestamp, contacts):
    """
    Busca si el indicativo ya existe en el mismo bloque OA.
    Retorna dict con info del contacto duplicado si existe, None si no.
    """
    block, _ = get_oa_block_from_utc(timestamp)
    for c in contacts:
        if c.get("callsign") == callsign:
            prev_block, prev_hora_oa = get_oa_block_from_utc(c.get("timestamp"))
            if prev_block == block:
                return {
                    "callsign": c.get("callsign"),
                    "name": c.get("name", "-"),
                    "hora_oa": prev_hora_oa,
                }
    return None
