from domain.repositories.contact_log_repository import ContactLogRepository
from domain.entities.operation_contact import OperationContact
from domain.entities.contest_contact import ContestContact
from domain.entities.contact_log import ContactLog
from domain.validators import LogValidator
from domain.contest_rules import ContestRules
from domain.operation_rules import OperationRules


def add_contact_to_log(
    db_path: str, log_id: str, contact_data: dict, contact_type: str = "operativo"
):
    """
    Agrega un contacto a un log existente (operativo o concurso) con validaciones de dominio.
    contact_data: diccionario con los datos del contacto.
    contact_type: 'operativo' u 'concurso'.
    """
    repo = ContactLogRepository(db_path)
    # Cargar contactos existentes para validación
    contacts = repo.get_contacts(log_id)
    if contact_type == "operativo":
        contact = OperationContact(**contact_data)
    elif contact_type == "concurso":
        contact = ContestContact(**contact_data)
    else:
        raise ValueError("Tipo de contacto no soportado")
    # Validaciones genéricas
    errors = LogValidator.validate_contact(contact, contacts)
    # Validaciones específicas
    if contact_type == "operativo":
        errors += OperationRules.validate(contact, contacts)
    elif contact_type == "concurso":
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
    contact_type: str = "operativo",
):
    """
    Actualiza un contacto existente en un log, validando antes de guardar.
    """
    repo = ContactLogRepository(db_path)
    contacts = repo.get_contacts(log_id)
    # Eliminar el contacto anterior
    repo.delete_contact(contact_id)
    # Crear y validar el nuevo contacto actualizado
    if contact_type == "operativo":
        contact = OperationContact(**updated_data)
    elif contact_type == "concurso":
        contact = ContestContact(**updated_data)
    else:
        raise ValueError("Tipo de contacto no soportado")
    # Validaciones genéricas
    errors = LogValidator.validate_contact(contact, contacts)
    # Validaciones específicas
    if contact_type == "operativo":
        errors += OperationRules.validate(contact, contacts)
    elif contact_type == "concurso":
        errors += ContestRules.validate(contact, contacts)
    if errors:
        raise ValueError("; ".join(errors))
    # Si todo es válido, guardar
    repo.save_contact(log_id, contact)
    return contact
