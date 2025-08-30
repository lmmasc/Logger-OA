"""
Utilidades de texto para normalización y extracción de datos de operadores.
Basado en la versión anterior, adaptado para la nueva estructura.
"""

import re
import unicodedata


def normalize_ascii(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    ).upper()


def normalize_callsign(raw: str) -> str:
    """
    Normaliza un indicativo a la forma canónica.
    """
    if not isinstance(raw, str):
        return ""
    raw = normalize_ascii(raw).strip()
    raw = re.sub(r"\s+", " ", raw)
    raw = re.sub(r"\s*-\s*", "-", raw)
    if "-" not in raw:
        return raw
    parts = raw.split("-")
    prefix = parts[0]
    suffix = "-".join(parts[1:]) if len(parts) > 1 else ""
    if not re.search(r"\d", prefix):
        return raw.replace("-", "")
    suffix_clean = suffix.replace("-", "")
    if re.search(r"\d", suffix_clean):
        return f"{prefix}/{suffix_clean}"
    return prefix + suffix_clean


def extract_cutoff_date(text: str) -> str | None:
    m = re.search(
        r"AL\s+(\d{1,2})\s+([A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1]+)\s+(\d{4})",
        text,
        re.IGNORECASE,
    )
    if m:
        day, month, year = m.groups()
        months = {
            "ENERO": "01",
            "FEBRERO": "02",
            "MARZO": "03",
            "ABRIL": "04",
            "MAYO": "05",
            "JUNIO": "06",
            "JULIO": "07",
            "AGOSTO": "08",
            "SETIEMBRE": "09",
            "SEPTIEMBRE": "09",
            "OCTUBRE": "10",
            "NOVIEMBRE": "11",
            "DICIEMBRE": "12",
        }
        month_num = months.get(normalize_ascii(month), "01")
        return f"{int(day):02d}/{month_num}/{year}"
    return None
