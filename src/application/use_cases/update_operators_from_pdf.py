"""
Orquestador del proceso de actualización de operadores desde PDF.
"""

from infrastructure.pdf.pdf_extractor import extract_operators_from_pdf
from infrastructure.db.data_normalizer import normalize_operator_data
from infrastructure.db.db_integrator import integrate_operators_to_db


def update_operators_from_pdf(pdf_path):
    """
    Ejecuta el flujo completo de extracción, normalización e integración.
    """
    from infrastructure.db.queries import get_radio_operators, update_radio_operator
    from config.paths import get_database_path
    from datetime import datetime, timezone, timedelta

    raw_data = extract_operators_from_pdf(pdf_path)
    normalized_data = normalize_operator_data(raw_data)

    # 1. Mapear operadores nuevos por callsign
    new_map = {op["callsign"]: op for op in normalized_data}

    # 2. Obtener existentes
    db_path = get_database_path()
    existing_rows = get_radio_operators()
    existing = {}

    def to_int_or_none(val):
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            try:
                return int(val) if val.isdigit() else None
            except Exception:
                return None
        return None

    for row in existing_rows:
        (
            callsign,
            name,
            category,
            type_,
            region,
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
            "region": region,
            "district": district,
            "province": province,
            "department": department,
            "license": license_,
            "resolution": resolution,
            "expiration_date": to_int_or_none(expiration_date),
            "cutoff_date": to_int_or_none(cutoff_date),
            "enabled": enabled,
            "country": country,
            "updated_at": to_int_or_none(updated_at),
        }

    now = int(datetime.now(timezone.utc).timestamp())
    to_upsert = []
    # --- NUEVO: Inicializar contadores ---
    total = len(normalized_data)
    new = 0
    updated = 0
    disabled = 0
    reenabled = 0
    protected = 0  # Contador de registros que no se inhabilitan por protección
    unchanged = 0  # Contador de registros sin cambios
    # 3. Procesar nuevos y actualizar existentes
    for cs, op in new_map.items():
        op = op.copy()
        op["enabled"] = 1
        op["updated_at"] = now
        if cs in existing:
            prev_exp = existing[cs].get("expiration_date", None)
            new_exp = op.get("expiration_date", None)
            prev_cutoff = existing[cs].get("cutoff_date", None)
            prev_updated = existing[cs].get("updated_at", None)
            d_prev = prev_exp
            d_new = new_exp
            d_cutoff_pdf = op.get("cutoff_date", None)
            d_updated_prev = prev_updated
            # Comprobar si hay cambios en campos relevantes
            fields_to_check = [
                "name",
                "category",
                "type",
                "region",
                "district",
                "province",
                "department",
                "license",
                "resolution",
                "expiration_date",
            ]
            changed = any(op.get(f) != existing[cs].get(f) for f in fields_to_check)
            # Solo actualizar si la info es más nueva y hay cambios
            if d_cutoff_pdf and d_updated_prev and d_cutoff_pdf < d_updated_prev:
                unchanged += 1
                op["enabled"] = existing[cs]["enabled"]
            elif d_new and (not d_prev or d_new > d_prev):
                op["enabled"] = 1
                updated += 1
            elif changed:
                if (
                    not d_cutoff_pdf
                    or not d_updated_prev
                    or d_cutoff_pdf >= d_updated_prev
                ):
                    op["enabled"] = 1
                    updated += 1
                else:
                    unchanged += 1
                    op["enabled"] = existing[cs]["enabled"]
            elif existing[cs]["enabled"] != 1:
                op["enabled"] = 1
                reenabled += 1
            else:
                unchanged += 1
                op["enabled"] = existing[cs]["enabled"]
        else:
            new += 1
        to_upsert.append(op)

    # Obtener la fecha de corte del PDF (asumimos que todos los registros tienen la misma)
    cutoff_date_pdf = None
    if normalized_data and "cutoff_date" in normalized_data[0]:
        cutoff_date_pdf = normalized_data[0]["cutoff_date"]

    # 4. Deshabilitar OA ausentes
    for cs, op in existing.items():
        if cs.upper().startswith("OA") and cs not in new_map and op["enabled"] != 0:
            can_disable = True
            if cutoff_date_pdf:
                d_cutoff = cutoff_date_pdf
                updated_at = op.get("updated_at", None)
                expiration = op.get("expiration_date", None)
                d_updated = updated_at
                d_exp = expiration
                if (d_updated and d_cutoff and d_cutoff < d_updated) or (
                    d_exp and d_cutoff and d_exp > d_cutoff
                ):
                    can_disable = False
            if can_disable:
                op = op.copy()
                op["enabled"] = 0
                op["updated_at"] = now
                to_upsert.append(op)
                disabled += 1
            else:
                protected += 1

    result = integrate_operators_to_db(to_upsert)

    # --- CHEQUEO POST-IMPORTACIÓN: deshabilitar vencidos ---
    from infrastructure.db.queries import disable_expired_operators

    try:
        expired_disabled = disable_expired_operators()
    except Exception:
        expired_disabled = 0

    # --- NUEVO: Retornar resumen ---
    summary = {
        "total": total,
        "new": new,
        "updated": updated,
        "unchanged": unchanged,
        "disabled": disabled,
        "reenabled": reenabled,
        "protected": protected,
        "ok": result,
        "expired_disabled": expired_disabled,
    }
    return summary
