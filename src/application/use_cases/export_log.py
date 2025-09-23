import csv
import os
from domain.repositories.contact_log_repository import ContactLogRepository
from config.paths import get_export_dir
from utils.resources import get_resource_path
from interface_adapters.ui.view_manager import LogType
from config.settings_service import LanguageValue
from typing import Optional


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
    # Formatear start_time como fecha local desde timestamp
    from config.paths import format_timestamp_local

    fecha_local = format_timestamp_local(start_time)
    # Headers y campos como en ContactTableWidget
    # Usar fecha_local donde se requiera mostrar la fecha
    # ...existing code...
    # Comparar directamente con Enum
    # Definición de campos y traducciones diferenciadas para exportación TXT
    EXPORT_TXT_CONTEST_FIELDS = [
        {"key": "callsign", "translation": "log_contest_export_txt_header_callsign"},
        {"key": "name", "translation": "log_contest_export_txt_header_name"},
        {"key": "region", "translation": "log_contest_export_txt_header_region"},
        {"key": "qtr_oa", "translation": "log_contest_export_txt_header_qtr_oa"},
        {"key": "rs_rx", "translation": "log_contest_export_txt_header_rs_rx"},
        {
            "key": "exchange_received",
            "translation": "log_contest_export_txt_header_exchange_received",
        },
        {"key": "rs_tx", "translation": "log_contest_export_txt_header_rs_tx"},
        {
            "key": "exchange_sent",
            "translation": "log_contest_export_txt_header_exchange_sent",
        },
        {
            "key": "obs",
            "translation": "log_contest_export_txt_header_observations",
        },
    ]
    EXPORT_TXT_OPERATIVE_FIELDS = [
        {"key": "callsign", "translation": "log_operative_export_txt_header_callsign"},
        {"key": "name", "translation": "log_operative_export_txt_header_name"},
        {"key": "country", "translation": "log_operative_export_txt_header_country"},
        {"key": "region", "translation": "log_operative_export_txt_header_region"},
        {"key": "station", "translation": "log_operative_export_txt_header_station"},
        {"key": "energy", "translation": "log_operative_export_txt_header_energy"},
        {"key": "power", "translation": "log_operative_export_txt_header_power"},
        {"key": "rs_rx", "translation": "log_operative_export_txt_header_rs_rx"},
        {"key": "rs_tx", "translation": "log_operative_export_txt_header_rs_tx"},
        {"key": "qtr_oa", "translation": "log_operative_export_txt_header_qtr_oa"},
        {"key": "qtr_utc", "translation": "log_operative_export_txt_header_qtr_utc"},
        {"key": "obs", "translation": "log_operative_export_txt_header_obs"},
    ]
    if log_type == LogType.CONTEST_LOG.value:
        headers = [
            translation_service.tr(f["translation"]) for f in EXPORT_TXT_CONTEST_FIELDS
        ]
        fieldnames = [f["key"] for f in EXPORT_TXT_CONTEST_FIELDS]
    elif log_type == LogType.OPERATION_LOG.value:
        headers = [
            translation_service.tr(f["translation"])
            for f in EXPORT_TXT_OPERATIVE_FIELDS
        ]
        fieldnames = [f["key"] for f in EXPORT_TXT_OPERATIVE_FIELDS]
    else:
        raise ValueError(f"Tipo de log no soportado para exportación: {log_type}")
    # ...existing code...
    # Procesar filas como en la UI
    import datetime

    date_fmt = "%d/%m/%Y"
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
                        if log_type == LogType.CONTEST_LOG.value:
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
                elif log_type == LogType.CONTEST_LOG.value and key in (
                    "exchange_received",
                    "exchange_sent",
                ):
                    val = contact.get(key, "")
                    row.append(str(val).zfill(3) if val else "")
                elif key == "country":
                    from domain.callsign_utils import get_country_full_name

                    lang = "es"
                    if hasattr(translation_service, "get_language"):
                        lang_enum = translation_service.get_language()
                        lang = getattr(lang_enum, "value", str(lang_enum))
                    itu_code = str(contact.get(key, ""))
                    from utils.text import normalize_ascii

                    country_name = get_country_full_name(itu_code, lang) or itu_code
                    row.append(normalize_ascii(country_name))
                else:
                    row.append(str(contact.get(key, "")))
            txtfile.write("\t".join(row) + "\n")
    return export_path


def export_log_to_csv(
    db_path: str, export_filename: Optional[str] = None, translation_service=None
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
    # ...existing code...
    # Comparar directamente con Enum
    # Definición de campos y traducciones diferenciadas para exportación CSV
    EXPORT_CSV_CONTEST_FIELDS = [
        {"key": "callsign", "translation": "log_contest_export_csv_header_callsign"},
        {"key": "name", "translation": "log_contest_export_csv_header_name"},
        {"key": "region", "translation": "log_contest_export_csv_header_region"},
        {"key": "qtr_oa", "translation": "log_contest_export_csv_header_qtr_oa"},
        {"key": "rs_rx", "translation": "log_contest_export_csv_header_rs_rx"},
        {
            "key": "exchange_received",
            "translation": "log_contest_export_csv_header_exchange_received",
        },
        {"key": "rs_tx", "translation": "log_contest_export_csv_header_rs_tx"},
        {
            "key": "exchange_sent",
            "translation": "log_contest_export_csv_header_exchange_sent",
        },
        {
            "key": "obs",
            "translation": "log_contest_export_csv_header_observations",
        },
    ]
    EXPORT_CSV_OPERATIVE_FIELDS = [
        {"key": "callsign", "translation": "log_operative_export_csv_header_callsign"},
        {"key": "name", "translation": "log_operative_export_csv_header_name"},
        {"key": "country", "translation": "log_operative_export_csv_header_country"},
        {"key": "region", "translation": "log_operative_export_csv_header_region"},
        {"key": "station", "translation": "log_operative_export_csv_header_station"},
        {"key": "energy", "translation": "log_operative_export_csv_header_energy"},
        {"key": "power", "translation": "log_operative_export_csv_header_power"},
        {"key": "rs_rx", "translation": "log_operative_export_csv_header_rs_rx"},
        {"key": "rs_tx", "translation": "log_operative_export_csv_header_rs_tx"},
        {"key": "qtr_oa", "translation": "log_operative_export_csv_header_qtr_oa"},
        {"key": "qtr_utc", "translation": "log_operative_export_csv_header_qtr_utc"},
        {"key": "obs", "translation": "log_operative_export_csv_header_obs"},
    ]
    if log_type == LogType.CONTEST_LOG.value:
        headers = [
            translation_service.tr(f["translation"]) for f in EXPORT_CSV_CONTEST_FIELDS
        ]
        fieldnames = [f["key"] for f in EXPORT_CSV_CONTEST_FIELDS]
    elif log_type == LogType.OPERATION_LOG.value:
        headers = [
            translation_service.tr(f["translation"])
            for f in EXPORT_CSV_OPERATIVE_FIELDS
        ]
        fieldnames = [f["key"] for f in EXPORT_CSV_OPERATIVE_FIELDS]
    else:
        raise ValueError(f"Tipo de log no soportado para exportación: {log_type}")
    # ...existing code...
    # Procesar filas como en la UI
    import datetime

    date_fmt = "%d/%m/%Y"
    # Determinar nombre de archivo
    if not export_filename:
        from config.paths import format_timestamp_local

        fecha_local = format_timestamp_local(start_time)
        export_filename = f"{operator}_{log_type}_{fecha_local}.csv"
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
                        if log_type == LogType.CONTEST_LOG.value:
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
                elif log_type == LogType.CONTEST_LOG.value and key in (
                    "exchange_received",
                    "exchange_sent",
                ):
                    val = contact.get(key, "")
                    row.append(str(val).zfill(3) if val else "")
                elif key == "country":
                    from domain.callsign_utils import get_country_full_name

                    lang = "es"
                    if hasattr(translation_service, "get_language"):
                        lang_enum = translation_service.get_language()
                        lang = getattr(lang_enum, "value", str(lang_enum))
                    itu_code = str(contact.get(key, ""))
                    from utils.text import normalize_ascii

                    country_name = get_country_full_name(itu_code, lang) or itu_code
                    row.append(normalize_ascii(country_name))
                else:
                    row.append(str(contact.get(key, "")))
            writer.writerow(row)
    return export_path


def export_log_to_adi(db_path: str, export_path: str) -> str:
    """
    Exporta el log a un archivo ADI (ADIF) usando los campos mínimos recomendados.
    """
    import sqlite3
    from domain.repositories.contact_log_repository import ContactLogRepository
    import datetime

    import json

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
        metadata = row[5]
    contacts = repo.get_contacts(log_id)
    if not contacts:
        raise ValueError("No hay contactos para exportar.")
    # Parse metadata for band/mode (operativos)
    band_meta = ""
    mode_meta = ""
    if metadata:
        try:
            meta_dict = json.loads(metadata)
            # Mapeo banda
            band_raw = meta_dict.get("frequency_band", "") or meta_dict.get("band", "")
            if band_raw == "band_hf":
                band_meta = "40M"
            elif band_raw == "band_vhf":
                band_meta = "2M"
            elif band_raw == "band_uhf":
                band_meta = "70CM"
            else:
                band_meta = ""
            # Mapeo modo
            mode_raw = meta_dict.get("mode_key", "") or meta_dict.get("mode", "")
            if mode_raw == "mode_lsb":
                mode_meta = "LSB"
            elif mode_raw == "mode_usb":
                mode_meta = "USB"
            elif mode_raw == "mode_fm":
                mode_meta = "FM"
            else:
                mode_meta = ""
        except Exception:
            pass
    # Generar ADIF
    adif_lines = []
    adif_lines.append(
        f"<ADIF_VER:5>3.1.0 <STATION_CALLSIGN:{len(operator)}>{operator} <EOH>"
    )
    for contact in contacts:
        # Campos mínimos
        callsign = contact.get("callsign", "")
        ts = contact.get("timestamp", None)
        if ts:
            dt_utc = datetime.datetime.fromtimestamp(int(ts), tz=datetime.timezone.utc)
            qso_date = dt_utc.strftime("%Y%m%d")
            time_on = dt_utc.strftime("%H%M%S")
        else:
            qso_date = ""
            time_on = ""
        # Banda y modo
        if log_type == LogType.CONTEST_LOG.value:
            band = "40M"
            mode = "SSB"
        else:
            band = band_meta
            mode = mode_meta
        rst_sent = contact.get("rs_tx", "") or contact.get("exchange_sent", "")
        rst_rcvd = contact.get("rs_rx", "") or contact.get("exchange_received", "")
        # Construir línea ADIF
        adif_entry = (
            f"<CALL:{len(callsign)}>{callsign} "
            f"<QSO_DATE:{len(qso_date)}>{qso_date} "
            f"<TIME_ON:{len(time_on)}>{time_on} "
            f"<BAND:{len(band)}>{band} "
            f"<MODE:{len(mode)}>{mode} "
            f"<RST_SENT:{len(rst_sent)}>{rst_sent} "
            f"<RST_RCVD:{len(rst_rcvd)}>{rst_rcvd} <EOR>"
        )
        adif_lines.append(adif_entry)
    with open(export_path, "w", encoding="utf-8") as adif_file:
        adif_file.write("\n".join(adif_lines))
    return export_path


def export_log_to_pdf(db_path: str, export_path: str) -> str:
    """
    Exporta el log a un archivo PDF con formato de planilla de concursos OA-HF.
    """
    import sqlite3
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
    )
    from reportlab.lib.styles import getSampleStyleSheet
    from infrastructure.db.queries import get_radio_operator_by_callsign
    from translation.translation_service import translation_service as ts
    import datetime

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
        metadata = row[5]
    # Solo soporta logs de concurso
    from translation.translation_service import translation_service as ts

    if log_type != LogType.CONTEST_LOG.value:
        raise ValueError("Exportación a PDF solo soportada para logs de concurso.")
    contacts = repo.get_contacts(log_id)
    if not contacts:
        raise ValueError("No hay contactos para exportar.")
    # ...existing code for PDF generation...
    # Obtener datos del operador
    op_data = get_radio_operator_by_callsign(operator)
    op_name = op_data[1] if op_data else ""
    op_category = op_data[2] if op_data else ""
    op_region = op_data[4] if op_data else ""

    # Obtener nombre de concurso traducido
    contest_name = ""
    if metadata:
        import json

        try:
            meta_dict = json.loads(metadata)
            contest_key = meta_dict.get("contest_name_key", "")
            contest_name = ts.tr(contest_key) if contest_key else ""
        except Exception:
            pass

    # Formatear fecha local desde timestamp
    from config.paths import format_timestamp_local

    fecha = format_timestamp_local(start_time)

    # Construir cabecera con cuadricula y ancho total
    cabecera_labels = [
        "CONCURSO:",
        "Fecha:",
        "Indicativo:",
        "Categoría:",
        "Nombre:",
        "QTH:",
    ]
    cabecera_values = [contest_name, fecha, operator, op_category, op_name, op_region]
    cabecera_table = [
        [label, value] for label, value in zip(cabecera_labels, cabecera_values)
    ]

    # Ajustar ancho de cabecera y tabla
    from reportlab.lib.units import mm

    page_width = A4[0] - 2 * 20 * mm  # 20mm margen
    col_widths_cabecera = [page_width * 0.25, page_width * 0.75]
    col_widths_tabla = [
        page_width * 0.07,
        page_width * 0.15,
        page_width * 0.18,
        page_width * 0.18,
        page_width * 0.18,
        page_width * 0.24,
    ]

    # Construir tabla de contactos
    tabla = [["Nº", "QTR", "ESTACIÓN", "ENVIADO", "RECIBIDO", "OBSERVACIONES"]]
    for idx, contact in enumerate(contacts, 1):
        # QTR OA
        ts_contact = contact.get("timestamp", None)
        qtr = ""
        if ts_contact:
            dt_utc = datetime.datetime.fromtimestamp(
                int(ts_contact), tz=datetime.timezone.utc
            )
            dt_oa = dt_utc - datetime.timedelta(hours=5)
            qtr = dt_oa.strftime("%H:%M")
        estacion = contact.get("callsign", operator)
        # Enviado y recibido
        try:
            exchange_tx_num = int(contact.get("exchange_sent", 0))
        except Exception:
            exchange_tx_num = 0
        rs_tx = str(contact.get("rs_tx", "")).zfill(2)
        exchange_tx = str(exchange_tx_num).zfill(3)
        enviado = rs_tx + exchange_tx
        try:
            exchange_rx_num = int(contact.get("exchange_received", 0))
        except Exception:
            exchange_rx_num = 0
        rs_rx = str(contact.get("rs_rx", "")).zfill(2)
        exchange_rx = str(exchange_rx_num).zfill(3)
        recibido = rs_rx + exchange_rx
        observaciones = contact.get("obs", "")
        tabla.append([str(idx), qtr, estacion, enviado, recibido, observaciones])

    # Crear PDF
    doc = SimpleDocTemplate(
        export_path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    elements = []
    # Cabecera con cuadricula
    t_cabecera = Table(cabecera_table, colWidths=col_widths_cabecera)
    t_cabecera.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
            ]
        )
    )
    elements.append(t_cabecera)
    elements.append(Spacer(1, 12))
    # Tabla de contactos con ancho total
    t = Table(tabla, colWidths=col_widths_tabla, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
            ]
        )
    )
    elements.append(t)
    doc.build(elements)
    return export_path
