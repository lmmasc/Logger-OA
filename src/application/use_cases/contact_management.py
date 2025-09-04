from src.domain.repositories.contact_log_repository import ContactLogRepository
from src.domain.entities.operation_contact import OperationContact
from src.domain.entities.contest_contact import ContestContact


def add_contact_to_log(
    db_path: str, log_id: str, contact_data: dict, contact_type: str = "operativo"
):
    """
    Agrega un contacto a un log existente (operativo o concurso).
    contact_data: diccionario con los datos del contacto.
    contact_type: 'operativo' u 'concurso'.
    """
    repo = ContactLogRepository(db_path)
    if contact_type == "operativo":
        contact = OperationContact(**contact_data)
    elif contact_type == "concurso":
        contact = ContestContact(**contact_data)
    else:
        raise ValueError("Tipo de contacto no soportado")
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
    Actualiza un contacto existente en un log.
    """
    repo = ContactLogRepository(db_path)
    # Eliminar el contacto anterior
    repo.delete_contact(contact_id)
    # Crear y guardar el nuevo contacto actualizado
    if contact_type == "operativo":
        contact = OperationContact(**updated_data)
    elif contact_type == "concurso":
        contact = ContestContact(**updated_data)
    else:
        raise ValueError("Tipo de contacto no soportado")
    repo.save_contact(log_id, contact)
    return contact
