import csv
import os
from domain.repositories.contact_log_repository import ContactLogRepository
from config.paths import get_export_dir
from utils.resources import get_resource_path


def export_log_to_txt(db_path: str, export_path: str, translation_service=None) -> str:
    """
    Exporta el log a un archivo TXT, detectando tipo de log y usando cabeceras traducidas.
    """
    import sqlite3
    from importlib import import_module

    repo = ContactLogRepository(db_path)
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
    contacts = repo.get_contacts(log_id)
    if not contacts:
        raise ValueError("No hay contactos para exportar.")
    # Detectar idioma
    if translation_service is None:
        from translation.translation_service import translation_service as ts

        translation_service = ts
    lang = translation_service.get_language()
    # Headers y campos como en ContactTableWidget
    print(f"[EXPORT][DEBUG] log_type recibido: {log_type}")
    log_type_normalized = str(log_type).lower()
    # contest_types y operation_types como antes
    contest_types = ("concurso", "contest", "contest_log", "contestlog")
    operation_types = ("operativo", "ops", "operation_log", "operationlog")
    is_contest = log_type_normalized in contest_types
    print(f"[EXPORT][DEBUG] is_contest: {is_contest}")
    if is_contest:
        headers = [
            translation_service.tr("table_header_callsign"),
            translation_service.tr("name"),
            translation_service.tr("region"),
            "QTR",
            translation_service.tr("rs_rx"),
            translation_service.tr("table_header_exchange_rx"),
            translation_service.tr("rs_tx"),
            translation_service.tr("table_header_exchange_tx"),
            translation_service.tr("observations"),
        ]
        fieldnames = [
            "callsign",
            "name",
            "region",
            "qtr_oa",
            "rs_rx",
            "exchange_received",
            "rs_tx",
            "exchange_sent",
            "observations",
        ]
    else:
        headers = [
            translation_service.tr("table_header_callsign"),
            translation_service.tr("name"),
            translation_service.tr("country"),
            translation_service.tr("region"),
            translation_service.tr("station"),
            translation_service.tr("energy"),
            translation_service.tr("table_header_power"),
            translation_service.tr("rs_rx"),
            translation_service.tr("rs_tx"),
            translation_service.tr("clock_oa_label"),
            translation_service.tr("clock_utc_label"),
            translation_service.tr("observations"),
        ]
        fieldnames = [
            "callsign",
            "name",
            "country",
            "region",
            "station",
            "energy",
            "power",
            "rs_rx",
            "rs_tx",
            "qtr_oa",
            "qtr_utc",
            "obs",
        ]
    print(f"[EXPORT][DEBUG] headers: {headers}")
    # Procesar filas como en la UI
    import datetime

    if lang == "es":
        date_fmt = "%d/%m/%Y"
    else:
        date_fmt = "%m/%d/%Y"
    with open(export_path, "w", encoding="utf-8") as txtfile:
        txtfile.write("\t".join(headers) + "\n")
        for contact in contacts:
            row = []
            for key in fieldnames:
                if key == "qtr_oa":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        dt_utc = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        )
                        dt_oa = dt_utc - datetime.timedelta(hours=5)
                        if log_type == "contest":
                            value = dt_oa.strftime("%H:%M")
                        else:
                            value = dt_oa.strftime(f"%H:%M {date_fmt}")
                    row.append(value)
                elif key == "qtr_utc":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        value = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        ).strftime(f"%H:%M {date_fmt}")
                    row.append(value)
                elif key in ("station", "energy"):
                    row.append(translation_service.tr(contact.get(key, "")))
                elif key == "power":
                    val = contact.get(key, "")
                    row.append(f"{val} W" if val else "")
                elif log_type == "contest" and key in (
                    "exchange_received",
                    "exchange_sent",
                ):
                    val = contact.get(key, "")
                    row.append(str(val).zfill(3) if val else "")
                else:
                    row.append(str(contact.get(key, "")))
            txtfile.write("\t".join(row) + "\n")
    return export_path


def export_log_to_csv(
    db_path: str, export_filename: str = None, translation_service=None
) -> str:
    """
    Exporta todos los contactos de un log a un archivo CSV en la carpeta de exportación, detectando tipo de log y usando cabeceras traducidas.
    """
    import sqlite3
    from importlib import import_module

    repo = ContactLogRepository(db_path)
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
    contacts = repo.get_contacts(log_id)
    if not contacts:
        raise ValueError("No hay contactos para exportar.")
    # Detectar idioma
    if translation_service is None:
        from translation.translation_service import translation_service as ts

        translation_service = ts
    lang = translation_service.get_language()
    # Headers y campos como en ContactTableWidget
    print(f"[EXPORT][DEBUG] log_type recibido: {log_type}")
    log_type_normalized = str(log_type).lower()
    # contest_types y operation_types como antes
    contest_types = ("concurso", "contest", "contest_log", "contestlog")
    operation_types = ("operativo", "ops", "operation_log", "operationlog")
    is_contest = log_type_normalized in contest_types
    print(f"[EXPORT][DEBUG] is_contest: {is_contest}")
    if is_contest:
        headers = [
            translation_service.tr("table_header_callsign"),
            translation_service.tr("name"),
            translation_service.tr("region"),
            "QTR",
            translation_service.tr("rs_rx"),
            translation_service.tr("table_header_exchange_rx"),
            translation_service.tr("rs_tx"),
            translation_service.tr("table_header_exchange_tx"),
            translation_service.tr("observations"),
        ]
        fieldnames = [
            "callsign",
            "name",
            "region",
            "qtr_oa",
            "rs_rx",
            "exchange_received",
            "rs_tx",
            "exchange_sent",
            "observations",
        ]
    else:
        headers = [
            translation_service.tr("table_header_callsign"),
            translation_service.tr("name"),
            translation_service.tr("country"),
            translation_service.tr("region"),
            translation_service.tr("station"),
            translation_service.tr("energy"),
            translation_service.tr("table_header_power"),
            translation_service.tr("rs_rx"),
            translation_service.tr("rs_tx"),
            translation_service.tr("clock_oa_label"),
            translation_service.tr("clock_utc_label"),
            translation_service.tr("observations"),
        ]
        fieldnames = [
            "callsign",
            "name",
            "country",
            "region",
            "station",
            "energy",
            "power",
            "rs_rx",
            "rs_tx",
            "qtr_oa",
            "qtr_utc",
            "obs",
        ]
    print(f"[EXPORT][DEBUG] headers: {headers}")
    # Procesar filas como en la UI
    import datetime

    if lang == "es":
        date_fmt = "%d/%m/%Y"
    else:
        date_fmt = "%m/%d/%Y"
    # Determinar nombre de archivo
    if not export_filename:
        export_filename = f"{operator}_{log_type}_{start_time}.csv"
    export_path = get_export_dir(export_filename)
    export_path = get_resource_path(export_path)
    with open(export_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)
        for contact in contacts:
            row = []
            for key in fieldnames:
                if key == "qtr_oa":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        dt_utc = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        )
                        dt_oa = dt_utc - datetime.timedelta(hours=5)
                        if log_type == "contest":
                            value = dt_oa.strftime("%H:%M")
                        else:
                            value = dt_oa.strftime(f"%H:%M {date_fmt}")
                    row.append(value)
                elif key == "qtr_utc":
                    ts = contact.get("timestamp", None)
                    value = ""
                    if ts:
                        value = datetime.datetime.fromtimestamp(
                            int(ts), tz=datetime.timezone.utc
                        ).strftime(f"%H:%M {date_fmt}")
                    row.append(value)
                elif key in ("station", "energy"):
                    row.append(translation_service.tr(contact.get(key, "")))
                elif key == "power":
                    val = contact.get(key, "")
                    row.append(f"{val} W" if val else "")
                elif log_type == "contest" and key in (
                    "exchange_received",
                    "exchange_sent",
                ):
                    val = contact.get(key, "")
                    row.append(str(val).zfill(3) if val else "")
                else:
                    row.append(str(contact.get(key, "")))
            writer.writerow(row)
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
