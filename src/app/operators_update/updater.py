"""
Orquestador del proceso de actualización de operadores desde PDF.
"""

from .pdf_extractor import extract_operators_from_pdf
from .data_normalizer import normalize_operator_data
from .db_integrator import integrate_operators_to_db


def update_operators_from_pdf(pdf_path):
    """
    Ejecuta el flujo completo de extracción, normalización e integración.
    """
    from app.db.queries import get_radio_operators, update_radio_operator
    from app.utils.file_manager import get_db_path
    from datetime import datetime

    raw_data = extract_operators_from_pdf(pdf_path)
    normalized_data = normalize_operator_data(raw_data)

    # 1. Mapear operadores nuevos por callsign
    new_map = {op["callsign"]: op for op in normalized_data}

    # 2. Obtener existentes
    db_path = get_db_path()
    existing_rows = get_radio_operators()
    existing = {}
    for row in existing_rows:
        # El orden debe coincidir con get_radio_operators()
        (
            callsign,
            name,
            category,
            type_,
            district,
            province,
            department,
            license_,
            resolution,
            expiration_date,
            cutoff_date,
            enabled,
            country,
            updated_at,
        ) = row
        existing[callsign] = {
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
            "enabled": enabled,
            "country": country,
            "updated_at": updated_at,
        }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_upsert = []
    # 3. Procesar nuevos y actualizar existentes
    for cs, op in new_map.items():
        op = op.copy()
        op["enabled"] = 1
        op["updated_at"] = now
        if cs in existing:
            # Si la fecha de vencimiento nueva es mayor, actualizar
            prev_exp = existing[cs].get("expiration_date", "")
            new_exp = op.get("expiration_date", "")
            try:
                d_prev = datetime.strptime(prev_exp, "%d/%m/%Y") if prev_exp else None
                d_new = datetime.strptime(new_exp, "%d/%m/%Y") if new_exp else None
            except Exception:
                d_prev = d_new = None
            if d_new and (not d_prev or d_new > d_prev):
                op["enabled"] = 1
            elif existing[cs]["enabled"] != 1:
                op["enabled"] = 1
            else:
                op["enabled"] = existing[cs]["enabled"]
        to_upsert.append(op)

    # 4. Deshabilitar OA ausentes
    for cs, op in existing.items():
        if cs.upper().startswith("OA") and cs not in new_map and op["enabled"] != 0:
            op = op.copy()
            op["enabled"] = 0
            op["updated_at"] = now
            to_upsert.append(op)

    result = integrate_operators_to_db(to_upsert)
    return result
