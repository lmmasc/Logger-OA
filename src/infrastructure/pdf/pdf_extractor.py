"""
Funciones para extraer datos de operadores desde archivos PDF.
Incluye soporte flexible para distintos formatos en español (p.ej., Uruguay CX).
"""

import pdfplumber
import re
import os
from datetime import datetime, timezone, timedelta
from utils.text import normalize_ascii, normalize_callsign, extract_cutoff_date
from utils.resources import get_resource_path
from domain.callsign_utils import callsign_to_country


def extract_operators_from_pdf(pdf_path):
    """
    Extrae los datos de operadores desde el PDF especificado.
    Retorna una lista de diccionarios con los datos crudos y normalizados.
    La extracción es robusta ante variaciones de formato y encabezados.
    """
    # Cabeceras base usadas por el formato genérico (Perú u otros con nombres similares)
    pdf_headers = [
        "indicativo",
        "nombre",
        "categoria",
        "tipo",
        "distrito",
        "provincia",
        "departamento",
        "licencia",
        "resolucion",
        "fecha",
    ]
    results = []
    seen_callsigns = set()
    pdf_path = get_resource_path(pdf_path)  # Adaptación universal
    with pdfplumber.open(pdf_path) as pdf:
        # Extraer fecha de corte del texto de la primera página
        try:
            first_text = pdf.pages[0].extract_text() or ""
        except Exception:
            first_text = ""
        cutoff = extract_cutoff_date(first_text) or ""
        # Si no se detecta en el contenido, intentar deducir del nombre del archivo (p. ej. "Vigentes julio 2025")
        if not cutoff:
            cutoff = _extract_cutoff_from_filename(os.path.basename(pdf_path)) or ""
        total_pages = len(pdf.pages)
        last_uru_indices = None  # Recordar mapeo para páginas sin cabecera
        for page_number, page in enumerate(pdf.pages, start=1):
            # Estrategias de extracción de tabla
            strategies = [
                {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "snap_tolerance": 3,
                    "join_tolerance": 3,
                },
                {},
                {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "text",
                    "text_tolerance": 6,
                },
                {
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                    "text_tolerance": 6,
                },
            ]

            def _norm_header(h):
                h = normalize_ascii(h or "").lower().replace("/", " ")
                # Normalizar toda secuencia de espacios y saltos de línea a un solo espacio
                h = re.sub(r"\s+", " ", h).strip()
                # Normalizaciones de sinónimos comunes en español
                h = h.replace("razon social", "nombre")
                h = h.replace("apellidos razon social", "apellidos")
                h = h.replace("fecha vencimiento", "fecha")
                h = h.replace("distintivo de llamada", "indicativo")
                h = h.replace("senal distintiva", "indicativo")
                return h

            def find_header_idx(table):
                """Detecta fila de cabecera ya sea genérica o formato Uruguay."""
                for ridx, row in enumerate(table):
                    norm = [_norm_header(str(c)) for c in row]
                    joined = "|".join(norm)
                    # Genérico: requiere estos cuatro tokens
                    generic_ok = all(
                        tok in joined
                        for tok in ["indicativo", "nombre", "categoria", "fecha"]
                    )
                    # Uruguay: requiere indicativo (por normalización), categoria y fecha, y además presencia de "permiso" o de columnas separadas de nombre
                    uru_ok = (
                        ("indicativo" in joined)
                        and ("categoria" in joined)
                        and ("fecha" in joined)
                        and (
                            "permiso" in joined
                            or "apellidos" in joined
                            or "nombres" in joined
                        )
                    )
                    if generic_ok or uru_ok:
                        return ridx
                return None

            page_had_rows = False
            for ts in strategies:
                try:
                    tables = page.extract_tables(table_settings=ts)
                except Exception:
                    tables = None
                for table in tables or []:
                    if not table or len(table) < 1:
                        continue
                    header_idx = find_header_idx(table)
                    header = (
                        [_norm_header(str(c)) for c in table[header_idx]]
                        if header_idx is not None
                        else []
                    )
                    # Intentar primero formato Uruguay (CX)
                    uru_indices = _map_uruguay_columns(header) if header else None
                    if not uru_indices and last_uru_indices is not None:
                        uru_indices = last_uru_indices
                    if uru_indices:
                        # Recordar para tablas futuras sin cabecera
                        last_uru_indices = uru_indices
                        start_row = (header_idx + 1) if header_idx is not None else 0
                        for row in table[start_row:]:
                            raw_callsign = _safe_cell(row, uru_indices.get("callsign"))
                            surname = _safe_cell(row, uru_indices.get("surname"))
                            names = _safe_cell(row, uru_indices.get("names"))
                            permiso = _safe_cell(row, uru_indices.get("permiso"))
                            categoria = _safe_cell(row, uru_indices.get("category"))
                            fecha = _safe_cell(row, uru_indices.get("fecha"))

                            full_name = (surname + " " + names).strip()

                            raw_cs_cell = (raw_callsign or "").upper().strip()
                            if not raw_cs_cell:
                                continue
                            m = re.search(
                                r"\b([A-Z0-9]*\d[A-Z0-9]*)-([A-Z0-9]+)\b", raw_cs_cell
                            )
                            cs_token = (
                                f"{m.group(1)}-{m.group(2)}" if m else raw_cs_cell
                            )
                            norm_cs = normalize_callsign(cs_token)
                            if not norm_cs or norm_cs in seen_callsigns:
                                continue

                            country = callsign_to_country(norm_cs) or ""
                            exp_ts = _parse_spanish_date_to_utc(fecha, country)
                            cutoff_ts = (
                                _parse_spanish_date_to_utc(cutoff, country)
                                if cutoff
                                else None
                            )

                            data_en = {
                                "callsign": norm_cs,
                                "name": full_name,
                                "category": categoria or "",
                                "type": permiso or "",
                                "district": "",
                                "province": "",
                                "department": "",
                                "license": "",
                                "resolution": "",
                                "expiration_date": exp_ts,
                                "cutoff_date": cutoff_ts,
                                "country": country or "",
                            }
                            results.append(data_en)
                            seen_callsigns.add(norm_cs)
                            page_had_rows = True
                    else:
                        # Fallback: formato genérico anterior
                        if header_idx is None:
                            continue
                        idx_map = []
                        for expected in pdf_headers:
                            found_idx = None
                            for i, h in enumerate(header):
                                if expected in h:
                                    found_idx = i
                                    break
                            idx_map.append(found_idx)
                        if any(x is None for x in idx_map):
                            continue
                        if len(set(idx_map)) != len(idx_map):
                            continue
                        for row in table[header_idx + 1 :]:
                            data_es = {}
                            for i in range(len(pdf_headers)):
                                idx = idx_map[i]
                                val = _safe_cell(row, idx)
                                data_es[pdf_headers[i]] = val
                            raw_cs_cell = (data_es.get("indicativo") or "").upper()
                            m = re.search(
                                r"\b([A-Z0-9]*\d[A-Z0-9]*)-([A-Z0-9]+)\b", raw_cs_cell
                            )
                            cs_token = (
                                f"{m.group(1)}-{m.group(2)}" if m else raw_cs_cell
                            )
                            norm_cs = normalize_callsign(cs_token)
                            if not norm_cs or norm_cs in seen_callsigns:
                                continue
                            exp_raw = data_es.get("fecha", "").strip()
                            # Intentar dd/mm/YYYY
                            exp_ts = _parse_spanish_date_to_utc(exp_raw, None)
                            cutoff_ts = (
                                _parse_spanish_date_to_utc(cutoff, None)
                                if cutoff
                                else None
                            )
                            country = callsign_to_country(norm_cs) or ""
                            data_en = {
                                "callsign": norm_cs,
                                "name": data_es.get("nombre", ""),
                                "category": data_es.get("categoria", ""),
                                "type": data_es.get("tipo", ""),
                                "district": data_es.get("distrito", ""),
                                "province": data_es.get("provincia", ""),
                                "department": data_es.get("departamento", ""),
                                "license": data_es.get("licencia", ""),
                                "resolution": data_es.get("resolucion", ""),
                                "expiration_date": exp_ts,
                                "cutoff_date": cutoff_ts,
                                "country": country or "",
                            }
                            results.append(data_en)
                            seen_callsigns.add(norm_cs)
                            page_had_rows = True
                if page_had_rows:
                    break
    return results


def _safe_cell(row, idx):
    if idx is None or idx >= len(row):
        return ""
    cell = row[idx]
    if isinstance(cell, str):
        return cell.strip()
    return str(cell).strip() if cell is not None else ""


def _map_uruguay_columns(header_row_norm):
    """
    Detecta y mapea columnas del formato Uruguay (CX):
    - Distintivo de Llamada
    - Permiso
    - Apellidos/Razón Social
    - Nombres
    - Categoria Actual
    - Fecha Vencimiento
    Retorna dict con índices o None si no coincide.
    """

    def find_idx(predicates):
        for i, h in enumerate(header_row_norm):
            if any(tok in h for tok in predicates):
                return i
        return None

    callsign_idx = find_idx(["indicativo", "distintivo", "llamada"])  # normalizado
    permiso_idx = find_idx(["permiso"])  # Comun / …
    surname_idx = find_idx(["apellidos"])  # "apellidos" (de "apellidos/razon social")
    names_idx = find_idx(["nombres"])  # nombres
    category_idx = find_idx(["categoria"])  # categoria actual
    fecha_idx = find_idx(["fecha"])  # fecha (vencimiento)

    # Mínimos requeridos para considerar formato Uruguay
    # Requerir explícitamente la columna "permiso" y al menos una columna de nombres
    required = [callsign_idx, category_idx, fecha_idx, permiso_idx]
    if any(x is None for x in required):
        return None
    if (surname_idx is None) and (names_idx is None):
        return None

    return {
        "callsign": callsign_idx,
        "permiso": permiso_idx,
        "surname": surname_idx or None,
        "names": names_idx or None,
        "category": category_idx,
        "fecha": fecha_idx,
    }


def _parse_spanish_date_to_utc(date_str: str, country_code: str | None) -> int | None:
    """
    Convierte fechas en español a timestamp UTC.
    Soporta formatos:
      - dd/mm/YYYY
      - dd Mon. YYYY (abreviaturas españolas: Ene., Feb., Mar., Abr., May., Jun., Jul., Ago., Sep./Set., Oct., Nov., Dic.)
      - dd Mes YYYY (mes completo en mayúsculas)
    Usa zona horaria local aproximada por país si se conoce:
      - URY: UTC-3
      - PER: UTC-5 (por compatibilidad histórica)
      - Otro o desconocido: UTC
    """
    if not date_str:
        return None
    s = normalize_ascii(date_str).strip()
    # Intentar dd/mm/YYYY
    m = re.search(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        d, mo, y = map(int, m.groups())
        try:
            dt = datetime(y, mo, d)
            tz = _tz_for_country(country_code)
            dt_loc = dt.replace(tzinfo=tz)
            return int(dt_loc.astimezone(timezone.utc).timestamp())
        except Exception:
            return None

    # Intentar dd Mon. YYYY (abreviado)
    m = re.search(r"^(\d{1,2})\s+([A-Z]{3,4})\.?\s+(\d{4})$", s)
    if m:
        d, mon_abbr, y = m.groups()
        mon_map = {
            "ENE": 1,
            "FEB": 2,
            "MAR": 3,
            "ABR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AGO": 8,
            "SEP": 9,
            "SET": 9,
            "OCT": 10,
            "NOV": 11,
            "DIC": 12,
        }
        mo = mon_map.get(mon_abbr[:3])
        if mo:
            try:
                dt = datetime(int(y), int(mo), int(d))
                tz = _tz_for_country(country_code)
                dt_loc = dt.replace(tzinfo=tz)
                return int(dt_loc.astimezone(timezone.utc).timestamp())
            except Exception:
                return None

    # Intentar dd MES YYYY (mes completo)
    m = re.search(r"^(\d{1,2})\s+([A-Z]+)\s+(\d{4})$", s)
    if m:
        d, mon_full, y = m.groups()
        month_full_map = {
            "ENERO": 1,
            "FEBRERO": 2,
            "MARZO": 3,
            "ABRIL": 4,
            "MAYO": 5,
            "JUNIO": 6,
            "JULIO": 7,
            "AGOSTO": 8,
            "SEPTIEMBRE": 9,
            "SETIEMBRE": 9,
            "OCTUBRE": 10,
            "NOVIEMBRE": 11,
            "DICIEMBRE": 12,
        }
        mo = month_full_map.get(mon_full)
        if mo:
            try:
                dt = datetime(int(y), int(mo), int(d))
                tz = _tz_for_country(country_code)
                dt_loc = dt.replace(tzinfo=tz)
                return int(dt_loc.astimezone(timezone.utc).timestamp())
            except Exception:
                return None
    # Intentar dd mm YYYY con espacios (numérico)
    m = re.search(r"^(\d{1,2})\s+(\d{1,2})\s+(\d{4})$", s)
    if m:
        d, mo, y = map(int, m.groups())
        try:
            dt = datetime(y, mo, d)
            tz = _tz_for_country(country_code)
            dt_loc = dt.replace(tzinfo=tz)
            return int(dt_loc.astimezone(timezone.utc).timestamp())
        except Exception:
            return None
    return None


def _tz_for_country(country_code: str | None):
    # Offset aproximado; para mayor precisión se podría usar zoneinfo si fuese necesario
    if country_code == "URY":
        return timezone(timedelta(hours=-3))
    if country_code == "PER":
        return timezone(timedelta(hours=-5))
    # Por defecto UTC
    return timezone.utc


def _extract_cutoff_from_filename(filename: str) -> str | None:
    """
    Intenta extraer fecha (dd/mm/YYYY) a partir de nombres como
    "Vigentes julio 2025" o "al 13 ago 2025" dentro del nombre de archivo.
    Retorna string dd/mm/YYYY o None si no se puede deducir.
    """
    name = normalize_ascii(filename).lower()
    # al 13 ago 2025
    m = re.search(r"al\s+(\d{1,2})\s+([a-z]{3,9})\.?\s+(\d{4})", name)
    if m:
        d, mon, y = m.groups()
        mm = _month_to_mm(mon)
        if mm:
            return f"{str(int(d)).zfill(2)}/{mm}/{y}"
    # vigentes julio 2025 -> usar 01/mes/año
    m = re.search(r"vigentes\s+([a-z]{3,9})\.?\s+(\d{4})", name)
    if m:
        mon, y = m.groups()
        mm = _month_to_mm(mon)
        if mm:
            return f"01/{mm}/{y}"
    return None


def _month_to_mm(token: str) -> str | None:
    t = normalize_ascii(token).upper()[:3]
    mp = {
        "ENE": "01",
        "FEB": "02",
        "MAR": "03",
        "ABR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AGO": "08",
        "SEP": "09",
        "SET": "09",
        "OCT": "10",
        "NOV": "11",
        "DIC": "12",
    }
    return mp.get(t)
