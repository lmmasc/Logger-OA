"""
Funciones para extraer datos de operadores desde archivos PDF.
"""

import pdfplumber
import re
from ..utils.text import normalize_ascii, normalize_callsign, extract_cutoff_date


def extract_operators_from_pdf(pdf_path):
    """
    Extrae los datos de operadores desde el PDF especificado.
    Retorna una lista de diccionarios con los datos crudos y normalizados.
    La extracción es robusta ante variaciones de formato y encabezados.
    """
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
    with pdfplumber.open(pdf_path) as pdf:
        # Extraer fecha de corte del texto de la primera página
        try:
            first_text = pdf.pages[0].extract_text() or ""
        except Exception:
            first_text = ""
        cutoff = extract_cutoff_date(first_text) or ""
        total_pages = len(pdf.pages)
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
                h = (
                    normalize_ascii(h or "")
                    .lower()
                    .replace("/", " ")
                    .replace("  ", " ")
                    .strip()
                )
                h = h.replace("razon social", "nombre").replace(
                    "fecha vencimiento", "fecha"
                )
                return h

            def find_header_idx(table):
                required_any = ["indicativo", "nombre", "categoria", "fecha"]
                for ridx, row in enumerate(table):
                    norm = [_norm_header(str(c)) for c in row]
                    joined = "|".join(norm)
                    if all(tok in joined for tok in required_any):
                        return ridx
                return None

            page_had_rows = False
            for ts in strategies:
                try:
                    tables = page.extract_tables(table_settings=ts)
                except Exception:
                    tables = None
                for table in tables or []:
                    if not table or len(table) < 2:
                        continue
                    header_idx = find_header_idx(table)
                    if header_idx is None:
                        continue
                    header = [_norm_header(str(c)) for c in table[header_idx]]
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
                            val = ""
                            if idx is not None and idx < len(row):
                                cell = row[idx]
                                if isinstance(cell, str):
                                    val = cell.strip()
                                elif cell is not None:
                                    val = str(cell).strip()
                            data_es[pdf_headers[i]] = val
                        raw_cs_cell = (data_es.get("indicativo") or "").upper()
                        m = re.search(
                            r"\b([A-Z0-9]*\d[A-Z0-9]*)-([A-Z0-9]+)\b", raw_cs_cell
                        )
                        cs_token = f"{m.group(1)}-{m.group(2)}" if m else raw_cs_cell
                        norm_cs = normalize_callsign(cs_token)
                        if not norm_cs or norm_cs in seen_callsigns:
                            continue
                        exp_raw = data_es.get("fecha", "")
                        mdate = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", exp_raw)
                        exp_date = mdate.group(1) if mdate else exp_raw.strip()
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
                            "expiration_date": exp_date,
                            "cutoff_date": cutoff,
                        }
                        results.append(data_en)
                        seen_callsigns.add(norm_cs)
                        page_had_rows = True
                if page_had_rows:
                    break
    return results
