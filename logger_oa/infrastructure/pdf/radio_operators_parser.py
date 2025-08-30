from __future__ import annotations

from typing import Callable, List, Dict, Any, Optional
import re

import pdfplumber

from ...utils.text import normalize_ascii, normalize_callsign, extract_cutoff_date


FieldsEN = [
    "callsign",
    "name",
    "category",
    "type",
    "district",
    "province",
    "department",
    "license",
    "resolution",
    "expiration_date",
]


def _norm_header(h: str) -> str:
    # Normalize accents to ASCII, then lowercase to match against lowercase tokens
    h = normalize_ascii(h or "")
    h = h.lower()
    h = h.replace("/", " ").replace("  ", " ").strip()
    # Map variants found in PDFs
    h = h.replace("razon social", "nombre")
    h = h.replace("fecha vencimiento", "fecha")
    return h


def extract_radio_operators_rows(
    pdf_path: str, progress_cb: Callable[[int, int], None] | None = None
) -> List[Dict[str, Any]]:
    """Extract rows from the OSIPTEL/MTT style PDF into English-keyed dicts.

    Returns a list of dicts with keys:
    callsign, name, category, type, district, province, department,
    license, resolution, expiration_date
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

    results: List[Dict[str, Any]] = []
    seen_callsigns: set[str] = set()
    with pdfplumber.open(pdf_path) as pdf:
        # Try to extract cutoff date from the first page text, attach to each row as 'cutoff_date' for downstream use
        try:
            first_text = pdf.pages[0].extract_text() or ""
        except Exception:
            first_text = ""
        cutoff = extract_cutoff_date(first_text) or ""
        total_pages = len(pdf.pages)
        for page_number, page in enumerate(pdf.pages, start=1):
            # Try multiple table extraction strategies to be robust to layout
            strategies = [
                # Prefer line-detected borders first (usually cleaner column splits)
                {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "snap_tolerance": 3,
                    "join_tolerance": 3,
                },
                {},  # defaults
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

            def find_header_idx(table: List[List[Optional[str]]]) -> Optional[int]:
                # Find the first row that looks like a header containing key tokens
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
                    # Build index map for expected headers (case-insensitive via normalized lowercase)
                    idx_map: list[int | None] = []
                    for expected in pdf_headers:
                        found_idx = None
                        for i, h in enumerate(header):
                            if expected in h:
                                found_idx = i
                                break
                        idx_map.append(found_idx)
                    if any(x is None for x in idx_map):
                        continue  # Not a matching table
                    # Reject tables where headers collapse into the same column (e.g., 'tipo distrito')
                    if len(set(idx_map)) != len(idx_map):
                        continue

                    # Map rows after header
                    for row in table[header_idx + 1 :]:
                        # Extract Spanish columns first
                        data_es: Dict[str, str] = {}
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

                        # Basic row validity: extract callsign token from possibly noisy cell
                        raw_cs_cell = (data_es.get("indicativo") or "").upper()
                        # Find a token like PREFIX-with-digits - SUFFIX (e.g., OA4-BAU, 4T1-ABC, OA8-ON5VLG)
                        m = re.search(
                            r"\b([A-Z0-9]*\d[A-Z0-9]*)-([A-Z0-9]+)\b", raw_cs_cell
                        )
                        cs_token = f"{m.group(1)}-{m.group(2)}" if m else raw_cs_cell
                        norm_cs = normalize_callsign(cs_token)
                        if not norm_cs or norm_cs in seen_callsigns:
                            continue
                        # Normalize expiration date if embedded within text
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
                    break  # don't try other strategies on this page
            if progress_cb is not None:
                progress_cb(page_number, total_pages)
    return results


__all__ = ["extract_radio_operators_rows"]
