import re
from typing import Tuple, Optional

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
    indicativo = raw.strip().upper()
    partes = indicativo.split("/")
    base = None
    prefijo = None
    sufijo = None
    # Buscar todas las partes que cumplen el patrón de base
    base_indices = [
        i
        for i, parte in enumerate(partes)
        if re.match(r"^[A-Z]{1,3}\d{1,2}[A-Z]*$", parte)
    ]
    if base_indices:
        base_idx = base_indices[-1]
        base = partes[base_idx]
        # Prefijo: si hay una parte antes del base
        if base_idx > 0:
            prefijo = partes[base_idx - 1]
        # Sufijo: solo si hay partes después del base
        if base_idx < len(partes) - 1:
            sufijo_candidatos = partes[base_idx + 1 :]
            sufijo = "/".join(sufijo_candidatos)
    else:
        # Si no se encontró base, asumir el primero
        if partes:
            base = partes[0]
            if len(partes) > 1:
                sufijo = "/".join(partes[1:])
    return base or "", prefijo, sufijo
