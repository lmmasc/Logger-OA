import re
from typing import Tuple, Optional


def parse_callsign(raw: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Extrae el indicativo base, prefijo y sufijo de un indicativo de radioaficionado.
    Ejemplos:
        OA4BAU -> base=OA4BAU, prefijo=None, sufijo=None
        OA4BAU/M -> base=OA4BAU, prefijo=None, sufijo=M
        CE3/OA4BAU -> base=OA4BAU, prefijo=CE3, sufijo=None
        CE3/OA4BAU/M -> base=OA4BAU, prefijo=CE3, sufijo=M
        OA4BAU/7 -> base=OA4BAU, prefijo=None, sufijo=7
    Args:
        raw (str): Indicativo ingresado
    Returns:
        Tuple[base, prefijo, sufijo]
    """
    if not isinstance(raw, str):
        return "", None, None
    indicativo = raw.strip().upper()
    # Prefijo: antes del /, si hay más de uno, el primero
    # Sufijo: después del /, si hay más de uno, el último
    # Base: lo que parece un indicativo (letras+numero+letras)
    # Ejemplo: CE3/OA4BAU/M -> prefijo=CE3, base=OA4BAU, sufijo=M
    partes = indicativo.split("/")
    base = None
    prefijo = None
    sufijo = None
    # Buscar el indicativo base (letras+numero+letras)
    for i, parte in enumerate(partes):
        if re.match(r"^[A-Z]{1,3}\d{1,2}[A-Z]{1,4}$", parte):
            base = parte
            if i > 0:
                prefijo = partes[0]
            if i < len(partes) - 1:
                sufijo = partes[-1]
            break
    # Si no se encontró base, asumir el primero
    if base is None and partes:
        base = partes[0]
        if len(partes) > 1:
            sufijo = partes[-1]
    return base or "", prefijo, sufijo
