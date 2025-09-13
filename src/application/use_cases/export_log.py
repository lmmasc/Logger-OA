import csv
import os
from domain.repositories.contact_log_repository import ContactLogRepository
from config.paths import get_export_dir
from utils.resources import get_resource_path


def export_log_to_txt(db_path: str, export_path: str) -> str:
    """
    Exporta el log a un archivo TXT. Implementación pendiente.
    """
    # TODO: Implementar exportación a TXT
    print(f"[EXPORT] TXT: {db_path} -> {export_path}")
    return export_path


def export_log_to_csv(db_path: str, export_filename: str = None) -> str:
    """
    Exporta todos los contactos de un log a un archivo CSV en la carpeta de exportación.
    Devuelve la ruta del archivo exportado.
    """
    repo = ContactLogRepository(db_path)
    # Obtener log principal
    import sqlite3

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
        operator = row[2]
        start_time = row[3]
    # Obtener contactos
    contacts = repo.get_contacts(log_id)
    if not contacts:
        raise ValueError("No hay contactos para exportar.")
    # Determinar nombre de archivo
    if not export_filename:
        export_filename = f"{operator}_{log_type}_{start_time}.csv"
    export_path = get_export_dir(export_filename)
    export_path = get_resource_path(export_path)
    # Escribir CSV
    with open(export_path, "w", newline="", encoding="utf-8") as csvfile:
        if hasattr(contacts[0], "__dataclass_fields__"):
            fieldnames = list(contacts[0].__dataclass_fields__.keys())
        else:
            fieldnames = list(contacts[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(
                contact.__dict__ if hasattr(contact, "__dict__") else contact
            )
    return export_path


def export_log_to_adi(db_path: str, export_path: str) -> str:
    """
    Exporta el log a un archivo ADI. Implementación pendiente.
    """
    # TODO: Implementar exportación a ADI
    print(f"[EXPORT] ADI: {db_path} -> {export_path}")
    return export_path


def export_log_to_pdf(db_path: str, export_path: str) -> str:
    """
    Exporta el log a un archivo PDF. Implementación pendiente.
    """
    # TODO: Implementar exportación a PDF
    print(f"[EXPORT] PDF: {db_path} -> {export_path}")
    return export_path
