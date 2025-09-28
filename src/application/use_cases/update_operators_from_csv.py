"""
Caso de uso para actualizar operadores desde archivo CSV exportado por la aplicación.
"""

from infrastructure.csv.csv_extractor import extract_operators_from_csv
from infrastructure.db.db_integrator import integrate_operators_to_db


def update_operators_from_csv(csv_path):
    """
    Ejecuta el flujo completo de extracción e integración desde CSV.
    Similar a la lógica de Excel/PDF para actualizar operadores.

    Args:
        csv_path (str): Ruta al archivo CSV

    Returns:
        dict: Resumen del proceso con contadores y estado
    """
    from infrastructure.db.queries import get_radio_operators
    from datetime import datetime, timezone

    try:
        # Extraer y normalizar datos del CSV
        normalized_data = extract_operators_from_csv(csv_path)

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
                "message": "No se encontraron datos válidos en el archivo CSV",
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
            op["updated_at"] = now

            if cs in existing:
                existing_op = existing[cs]

                # Verificar si hay cambios en campos relevantes
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
                    "cutoff_date",
                    "country",
                ]
                changed = any(op.get(f) != existing_op.get(f) for f in fields_to_check)

                # Manejar cambios en enabled
                csv_enabled = op.get("enabled", 1)
                db_enabled = existing_op.get("enabled", 1)

                if csv_enabled != db_enabled:
                    if csv_enabled == 1 and db_enabled == 0:
                        reenabled += 1
                    elif csv_enabled == 0 and db_enabled == 1:
                        disabled += 1
                    changed = True

                if changed:
                    to_upsert.append(op)
                    updated += 1
                else:
                    unchanged += 1

            else:
                # Operador nuevo
                new += 1
                to_upsert.append(op)

        # 4. Los operadores no presentes en el CSV se mantienen tal como están
        # (no los deshabilitamos automáticamente como en Excel/PDF porque
        # el CSV puede ser una exportación parcial o filtrada)

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
            "message": f"Procesamiento completado: {new} nuevos, {updated} actualizados",
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
            "message": f"Error procesando CSV: {str(e)}",
        }
