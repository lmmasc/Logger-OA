"""
Funciones para limpiar y normalizar los datos extraídos del PDF.
"""

from utils.text import normalize_ascii, normalize_callsign
import re


def normalize_operator_data(raw_data):
    """
    Recibe una lista de dicts crudos y retorna una lista de dicts normalizados y limpios.
    Aplica reglas de limpieza, normalización de indicativos y campos, y validación básica.
    """
    normalized = []
    for row in raw_data:
        callsign = normalize_callsign(row.get("callsign", ""))
        name = normalize_ascii(row.get("name", "")).upper()
        category = normalize_ascii(row.get("category", "")).upper()
        type_ = normalize_ascii(row.get("type", "")).upper()
        district = normalize_ascii(row.get("district", "")).upper()
        province = normalize_ascii(row.get("province", "")).upper()
        department = normalize_ascii(row.get("department", "")).upper()
        license_ = normalize_ascii(row.get("license", ""))
        resolution = normalize_ascii(row.get("resolution", ""))
        expiration_date = row.get("expiration_date", None)
        cutoff_date = row.get("cutoff_date", None)
        country = row.get("country", None)
        if not country or not country.strip():
            country = "PER"
        else:
            country = normalize_ascii(country).upper()
        # Validar que sean enteros (timestamp UTC)
        if expiration_date is not None and not isinstance(expiration_date, int):
            expiration_date = None
        if cutoff_date is not None and not isinstance(cutoff_date, int):
            cutoff_date = None
        region = (
            f"{department}-{province}-{district}"
            if department or province or district
            else ""
        )
        normalized.append(
            {
                "callsign": callsign,
                "name": name,
                "category": category,
                "type": type_,
                "region": region,
                "district": district,
                "province": province,
                "department": department,
                "license": license_,
                "resolution": resolution,
                "expiration_date": expiration_date,
                "cutoff_date": cutoff_date,
                "country": country,
            }
        )
    return normalized
