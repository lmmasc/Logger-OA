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
    from config.paths import get_db_path
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
            prev_exp = existing[cs].get("expiration_date", "")
            new_exp = op.get("expiration_date", "")
            prev_cutoff = existing[cs].get("cutoff_date", "")
            prev_updated = existing[cs].get("updated_at", "")
            try:
                d_prev = datetime.strptime(prev_exp, "%d/%m/%Y") if prev_exp else None
                d_new = datetime.strptime(new_exp, "%d/%m/%Y") if new_exp else None
                d_cutoff_pdf = (
                    datetime.strptime(op.get("cutoff_date", ""), "%d/%m/%Y")
                    if op.get("cutoff_date", "")
                    else None
                )
                d_updated_prev = (
                    datetime.strptime(prev_updated, "%Y-%m-%d %H:%M:%S")
                    if prev_updated
                    else None
                )
            except Exception:
                d_prev = d_new = d_cutoff_pdf = d_updated_prev = None
            # Comprobar si hay cambios en campos relevantes
            fields_to_check = [
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
            changed = any(op.get(f) != existing[cs].get(f) for f in fields_to_check)
            # Solo actualizar si la info es más nueva y hay cambios
            if d_cutoff_pdf and d_updated_prev and d_cutoff_pdf < d_updated_prev:
                # El PDF es más antiguo que el registro, no actualizar
                unchanged += 1
                op["enabled"] = existing[cs]["enabled"]
            elif d_new and (not d_prev or d_new > d_prev):
                # Vencimiento mayor: actualizar
                op["enabled"] = 1
                updated += 1
            elif changed:
                # Algún campo relevante cambió: actualizar solo si la info es más nueva o igual
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
            # Validar fechas antes de inhabilitar
            can_disable = True
            if cutoff_date_pdf:
                from datetime import datetime

                # Fecha de actualización del registro existente
                updated_at = op.get("updated_at", "")
                expiration = op.get("expiration_date", "")
                try:
                    d_cutoff = datetime.strptime(cutoff_date_pdf, "%d/%m/%Y")
                except Exception:
                    d_cutoff = None
                try:
                    d_updated = (
                        datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                        if updated_at
                        else None
                    )
                except Exception:
                    d_updated = None
                try:
                    d_exp = (
                        datetime.strptime(expiration, "%d/%m/%Y")
                        if expiration
                        else None
                    )
                except Exception:
                    d_exp = None
                # Solo inhabilitar si la fecha de corte es igual o posterior a la actualización y la fecha de vencimiento es menor o igual a la de corte
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
    }
    return summary
