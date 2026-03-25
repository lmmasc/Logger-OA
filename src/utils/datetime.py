"""
Funciones utilitarias para formateo de fechas y horas en Logger OA.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Union

PERU_TZ = timezone(timedelta(hours=-5))


def parse_utc_timestamp(ts: Optional[Union[int, float, str]]) -> int:
    """
    Normaliza timestamps guardados por distintas versiones de la app.

    Acepta epoch UTC entero/float y también strings legacy en hora local de Perú
    con formato ``YYYY-MM-DD_HH-MM-SS`` o ``YYYY-MM-DD HH:MM:SS``.
    """
    if ts is None or ts == "":
        return 0
    if isinstance(ts, bool):
        return int(ts)
    if isinstance(ts, (int, float)):
        return int(ts)

    value = str(ts).strip()
    if not value:
        return 0
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)

    for fmt in ("%Y-%m-%d_%H-%M-%S", "%Y-%m-%d %H:%M:%S"):
        try:
            dt_local = datetime.strptime(value, fmt).replace(tzinfo=PERU_TZ)
            return int(dt_local.astimezone(timezone.utc).timestamp())
        except ValueError:
            continue

    raise ValueError(f"Formato de timestamp no soportado: {ts}")


def format_iso_date(ts):
    """
    Convierte un timestamp UTC en string ISO (YYYY-MM-DD) en hora local de Perú.
    """
    if not ts:
        return ""
    dt_utc = datetime.fromtimestamp(parse_utc_timestamp(ts), timezone.utc)
    dt_peru = dt_utc.astimezone(PERU_TZ)
    return dt_peru.strftime("%Y-%m-%d")


def format_iso_datetime(ts):
    """
    Convierte un timestamp UTC en string ISO (YYYY-MM-DD HH:MM:SS) en hora local de Perú.
    """
    if not ts:
        return ""
    dt_utc = datetime.fromtimestamp(parse_utc_timestamp(ts), timezone.utc)
    dt_peru = dt_utc.astimezone(PERU_TZ)
    return dt_peru.strftime("%Y-%m-%d %H:%M:%S")
