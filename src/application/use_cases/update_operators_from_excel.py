"""
Orquestador del proceso de actualización de operadores desde Excel.
Similar al procesamiento de PDF peruano, maneja enabled/disabled basado en cutoff dates.
"""

from infrastructure.excel.excel_extractor import extract_operators_from_excel
from infrastructure.db.db_integrator import integrate_operators_to_db


def update_operators_from_excel(excel_path):
    """
    Ejecuta el flujo completo de extracción e integración desde Excel.
    Maneja la lógica de enabled/disabled similar al PDF peruano.

    Args:
        excel_path (str): Ruta al archivo Excel (.xlsx)

    Returns:
        dict: Resumen del proceso con contadores y estado
    """
    from infrastructure.db.queries import get_radio_operators
    from datetime import datetime, timezone

    try:
        # Los datos del extractor ya vienen normalizados y validados con cutoff_date
        normalized_data = extract_operators_from_excel(excel_path)

        if not normalized_data:
            return {
                "total": 0,
                "new": 0,
                "updated": 0,
                "unchanged": 0,
                "disabled": 0,
                "reenabled": 0,
                "protected": 0,
                "ok": True,
                "message": "No se encontraron datos válidos en el archivo Excel",
            }

        # 1. Mapear operadores nuevos por callsign
        new_map = {op["callsign"]: op for op in normalized_data}

        # 2. Obtener existentes (todos los operadores de la BD)
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

        # Contadores
        total = len(normalized_data)
        new = 0
        updated = 0
        disabled = 0
        reenabled = 0
        protected = 0
        unchanged = 0

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
                d_cutoff_excel = op.get("cutoff_date", None)

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

                # Lógica similar al PDF: solo actualizar si la info es más nueva y hay cambios
                if d_cutoff_excel and prev_updated and d_cutoff_excel < prev_updated:
                    unchanged += 1
                    op["enabled"] = existing[cs]["enabled"]
                elif new_exp and (not prev_exp or new_exp > prev_exp):
                    op["enabled"] = 1
                    updated += 1
                elif changed:
                    if (
                        not d_cutoff_excel
                        or not prev_updated
                        or d_cutoff_excel >= prev_updated
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

        # Obtener la fecha de corte del Excel (todos tienen la misma)
        cutoff_date_excel = None
        if normalized_data and "cutoff_date" in normalized_data[0]:
            cutoff_date_excel = normalized_data[0]["cutoff_date"]

        # 4. Deshabilitar operadores chilenos ausentes (similar a como se hace con OA)
        for cs, op in existing.items():
            # Solo deshabilitar operadores chilenos que no estén en la nueva lista
            if op["country"] == "CHL" and cs not in new_map and op["enabled"] != 0:

                can_disable = True
                if cutoff_date_excel:
                    updated_at = op.get("updated_at", None)
                    expiration = op.get("expiration_date", None)

                    # Proteger si fue actualizado después del cutoff o si expira después del cutoff
                    if (updated_at and cutoff_date_excel < updated_at) or (
                        expiration and expiration > cutoff_date_excel
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
            "message": f"Procesamiento completado: {new} nuevos, {updated} actualizados, {disabled} deshabilitados",
        }

        return summary

    except Exception as e:
        return {
            "total": 0,
            "new": 0,
            "updated": 0,
            "unchanged": 0,
            "disabled": 0,
            "reenabled": 0,
            "protected": 0,
            "ok": False,
            "message": f"Error procesando Excel: {str(e)}",
        }
