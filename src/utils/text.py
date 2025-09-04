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
        r"AL\s+(\d{1,2})\s+([A-Z\u00c1\u00c9\u00CD\u00d3\u00DA\u00d1]+)\s+(\d{4})",
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
        month_num = months.get(month.upper(), "")
        if month_num:
            return f"{day.zfill(2)}/{month_num}/{year}"
    return None


def filter_text_match(
    haystack, needle, ignore_case=True, ignore_accents=True
):  # noqa: C901
    """
    Devuelve True si needle está en haystack, con opciones para ignorar mayúsculas y tildes.
    """
    if ignore_case:
        haystack = haystack.lower()
        needle = needle.lower()
    if ignore_accents:
        haystack = (
            unicodedata.normalize("NFKD", haystack).encode("ASCII", "ignore").decode()
        )
        needle = (
            unicodedata.normalize("NFKD", needle).encode("ASCII", "ignore").decode()
        )
    return needle in haystack
