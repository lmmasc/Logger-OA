"""
Funciones utilitarias para formateo de fechas y horas en Logger OA.
"""

from datetime import datetime, timezone, timedelta

PERU_TZ = timezone(timedelta(hours=-5))


def format_iso_date(ts):
    """
    Convierte un timestamp UTC en string ISO (YYYY-MM-DD) en hora local de Perú.
    """
    if not ts:
        return ""
    dt_utc = datetime.fromtimestamp(int(ts), timezone.utc)
    dt_peru = dt_utc.astimezone(PERU_TZ)
    return dt_peru.strftime("%Y-%m-%d")


def format_iso_datetime(ts):
    """
    Convierte un timestamp UTC en string ISO (YYYY-MM-DD HH:MM:SS) en hora local de Perú.
    """
    if not ts:
        return ""
    dt_utc = datetime.fromtimestamp(int(ts), timezone.utc)
    dt_peru = dt_utc.astimezone(PERU_TZ)
    return dt_peru.strftime("%Y-%m-%d %H:%M:%S")
