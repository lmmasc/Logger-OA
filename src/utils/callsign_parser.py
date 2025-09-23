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
        OA2/EA4 -> base=EA4, prefijo=OA2, sufijo=None
        OA2/EA4/7/MM -> base=EA4, prefijo=OA2, sufijo=7/MM
    Args:
        raw (str): Indicativo ingresado
    Returns:
        Tuple[base, prefijo, sufijo]
    """
    if not isinstance(raw, str):
        return "", None, None
    callsign_str = raw.strip().upper()
    parts = callsign_str.split("/")
    base_callsign = None
    prefix = None
    suffix = None
    # Buscar todas las partes que cumplen el patrón de indicativo base
    base_indexes = [
        i
        for i, part in enumerate(parts)
        if re.match(r"^[A-Z]{1,3}\d{1,2}[A-Z]*$", part)
    ]
    if base_indexes:
        base_idx = base_indexes[-1]
        base_callsign = parts[base_idx]
        # Prefijo: si hay una parte antes del base
        if base_idx > 0:
            prefix = parts[base_idx - 1]
        # Sufijo: solo si hay partes después del base
        if base_idx < len(parts) - 1:
            suffix_candidates = parts[base_idx + 1 :]
            suffix = "/".join(suffix_candidates)
    else:
        # Si no se encontró base, asumir la primera parte
        if parts:
            base_callsign = parts[0]
            if len(parts) > 1:
                suffix = "/".join(parts[1:])
    return base_callsign or "", prefix, suffix
