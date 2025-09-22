# callsign_utils.py
# Utilidades para prefijos ITU y país de indicativo

from domain.itu_prefixes import ITU_PREFIXES
from domain.itu_country_names import ITU_COUNTRY_NAMES


def callsign_to_country(callsign: str) -> str | None:
    """
    Devuelve el país ITU para un indicativo dado.
    Args:
        callsign (str): Indicativo completo (puede incluir /).
    Returns:
        str | None: Código de país ITU o None si no se encuentra.
    """
    parts = callsign.split("/")
    sorted_parts = sorted(parts, key=len)
    for part in sorted_parts:
        upper_part = part.upper()
        if upper_part in ITU_PREFIXES:
            return ITU_PREFIXES[upper_part]
    for part in sorted_parts:
        for length in range(1, len(part) + 1):
            prefix = part[:length].upper()
            if prefix in ITU_PREFIXES:
                return ITU_PREFIXES[prefix]
    return None


def get_country_full_name(itu_code: str, lang: str = "es") -> str | None:
    """
    Devuelve el nombre completo del país según el código ITU y el idioma.
    Args:
        itu_code (str): Código ITU del país (ej: 'USA', 'ESP').
        lang (str): 'es' para español, 'en' para inglés. Por defecto 'es'.
    Returns:
        str | None: Nombre completo del país o None si no existe.
    """
    country = ITU_COUNTRY_NAMES.get(itu_code)
    if country:
        return country.get(lang)
    return None
