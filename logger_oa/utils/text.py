from __future__ import annotations

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
    Normalize a callsign token extracted from the PDF into a canonical form.

    Rules:
    - Input may look like "OA4-BAU" (local) or "OA8-ON5VLG" (foreign portable in OA8).
    - For local forms: remove the hyphen -> OA4BAU.
    - For foreign suffix containing digits: replace hyphen with slash -> OA8/ON5VLG.
    - Works with any alphanumeric prefix that includes at least one digit.
    - Trims spaces and removes diacritics.
    """
    if not isinstance(raw, str):
        return ""
    # Uppercase and remove diacritics, normalize spaces and hyphen spacing
    raw = normalize_ascii(raw).strip()
    raw = re.sub(r"\s+", " ", raw)
    raw = re.sub(r"\s*-\s*", "-", raw)

    if "-" not in raw:
        return raw

    # If multiple hyphens appear, consider the first as delimiter between prefix and suffix
    parts = raw.split("-")
    prefix = parts[0]
    suffix = "-".join(parts[1:]) if len(parts) > 1 else ""

    # Ensure prefix contains at least one digit (typical for region/zone), else just collapse hyphens
    if not re.search(r"\d", prefix):
        return raw.replace("-", "")

    # Clean any stray hyphens inside suffix
    suffix_clean = suffix.replace("-", "")

    # If suffix contains any digit, treat as foreign callsign -> use slash
    # Example: suffix "ON5VLG" -> foreign, OA8/ON5VLG
    if re.search(r"\d", suffix_clean):
        return f"{prefix}/{suffix_clean}"

    # Otherwise, local suffix (letters or portable flags like "/P"): concatenate
    return prefix + suffix_clean


def extract_cutoff_date(text: str) -> str | None:
    m = re.search(r"AL\s+(\d{1,2})\s+([A-ZÁÉÍÓÚÑ]+)\s+(\d{4})", text, re.IGNORECASE)
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


__all__ = ["normalize_ascii", "normalize_callsign", "extract_cutoff_date"]
