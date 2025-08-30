"""
Funciones para limpiar y normalizar los datos extraídos del PDF.
"""

from ..utils.text import normalize_ascii, normalize_callsign
import re


def normalize_operator_data(raw_data):
    """
    Recibe una lista de dicts crudos y retorna una lista de dicts normalizados y limpios.
    Aplica reglas de limpieza, normalización de indicativos y campos, y validación básica.
    """
    normalized = []
    for row in raw_data:
        callsign = normalize_callsign(row.get("callsign", ""))
        name = normalize_ascii(row.get("name", "")).title()
        category = normalize_ascii(row.get("category", "")).upper()
        type_ = normalize_ascii(row.get("type", "")).upper()
        district = normalize_ascii(row.get("district", "")).title()
        province = normalize_ascii(row.get("province", "")).title()
        department = normalize_ascii(row.get("department", "")).title()
        license_ = normalize_ascii(row.get("license", ""))
        resolution = normalize_ascii(row.get("resolution", ""))
        expiration_date = row.get("expiration_date", "")
        cutoff_date = row.get("cutoff_date", "")
        # Validar formato de fecha dd/mm/yyyy
        if expiration_date and not re.match(r"\d{2}/\d{2}/\d{4}", expiration_date):
            expiration_date = ""
        normalized.append(
            {
                "callsign": callsign,
                "name": name,
                "category": category,
                "type": type_,
                "district": district,
                "province": province,
                "department": department,
                "license": license_,
                "resolution": resolution,
                "expiration_date": expiration_date,
                "cutoff_date": cutoff_date,
            }
        )
    return normalized
