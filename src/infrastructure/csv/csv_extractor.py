"""
Extractor para archivos CSV exportados por la propia aplicación.
Lee y normaliza datos de operadores desde CSV con headers traducidos.
"""

import csv
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from domain.itu_country_names import ITU_COUNTRY_NAMES
from utils.text import normalize_ascii


def extract_operators_from_csv(csv_path: str) -> List[Dict[str, Any]]:
    """
    Extrae y normaliza operadores desde un archivo CSV exportado por la aplicación.

    Args:
        csv_path (str): Ruta al archivo CSV

    Returns:
        List[Dict[str, Any]]: Lista de operadores normalizados
    """
    operators = []

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            # Detectar automáticamente el dialecto del CSV
            sample = f.read(1024)
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except csv.Error:
                # Si no puede detectar el delimitador, usar coma por defecto
                delimiter = ","

            reader = csv.DictReader(f, delimiter=delimiter)

            # Mapear headers traducidos a claves internas
            field_mapping = _create_field_mapping(list(reader.fieldnames or []))

            for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                try:
                    operator = _normalize_operator_row(row, field_mapping, row_num)
                    if operator:
                        operators.append(operator)
                except Exception as e:
                    print(f"Error procesando fila {row_num}: {e}")
                    continue

    except Exception as e:
        raise Exception(f"Error leyendo archivo CSV: {e}")

    return operators


def _create_field_mapping(headers: List[str]) -> Dict[str, str]:
    """
    Crea mapeo de headers traducidos a claves internas.
    """
    # Mapeo de posibles headers traducidos (español/inglés) a claves internas
    mapping_table = {
        # Español
        "indicativo": "callsign",
        "nombre": "name",
        "categoría": "category",
        "categoria": "category",  # Sin tilde
        "tipo": "type",
        "región": "region",
        "region": "region",  # Sin tilde
        "distrito": "district",
        "provincia": "province",
        "departamento": "department",
        "licencia": "license",
        "resolución": "resolution",
        "resolucion": "resolution",  # Sin tilde
        "vencimiento": "expiration_date",
        "fecha corte": "cutoff_date",
        "habilitado": "enabled",
        "país": "country",
        "pais": "country",  # Sin tilde
        "actualizado": "updated_at",
        # Inglés
        "callsign": "callsign",
        "name": "name",
        "category": "category",
        "type": "type",
        "district": "district",
        "province": "province",
        "department": "department",
        "license": "license",
        "resolution": "resolution",
        "expiration date": "expiration_date",
        "cutoff date": "cutoff_date",
        "enabled": "enabled",
        "country": "country",
        "updated at": "updated_at",
    }

    field_mapping = {}
    for header in headers:
        if header:
            normalized_header = normalize_ascii(header.lower().strip()).lower()
            if normalized_header in mapping_table:
                field_mapping[header] = mapping_table[normalized_header]
            else:
                # Buscar coincidencias parciales
                for key, value in mapping_table.items():
                    if key in normalized_header or normalized_header in key:
                        field_mapping[header] = value
                        break

    return field_mapping


def _normalize_operator_row(
    row: Dict[str, str], field_mapping: Dict[str, str], row_num: int
) -> Optional[Dict[str, Any]]:
    """
    Normaliza una fila del CSV a formato interno.
    """
    operator = {}

    # Mapear campos básicos
    for csv_header, internal_key in field_mapping.items():
        value = row.get(csv_header, "").strip()

        if internal_key == "callsign":
            if not value:
                print(f"Fila {row_num}: Indicativo requerido")
                return None
            operator["callsign"] = value.upper()

        elif internal_key == "name":
            if not value:
                print(f"Fila {row_num}: Nombre requerido")
                return None
            operator["name"] = value

        elif internal_key == "category":
            # Normalizar categorías
            cat_mapping = {
                "novicio": "NOVICIO",
                "intermedio": "INTERMEDIO",
                "superior": "SUPERIOR",
                "no aplica": "NO_APLICA",
                "no_aplica": "NO_APLICA",
            }
            normalized_cat = cat_mapping.get(value.lower(), value.upper())
            operator["category"] = normalized_cat

        elif internal_key == "enabled":
            # Convertir SÍ/NO o YES/NO a 1/0
            enabled_mapping = {
                "sí": 1,
                "si": 1,
                "yes": 1,
                "1": 1,
                "true": 1,
                "no": 0,
                "0": 0,
                "false": 0,
            }
            operator["enabled"] = enabled_mapping.get(value.lower(), 1)

        elif internal_key == "country":
            # Convertir nombre de país a código ITU si es necesario
            if len(value) > 3:  # Probablemente es nombre completo
                country_code = _get_country_code_from_name(value)
                operator["country"] = country_code or value
            else:
                operator["country"] = value.upper()

        elif internal_key in ("expiration_date", "cutoff_date"):
            # Convertir fecha DD/MM/YYYY a timestamp
            if value:
                try:
                    # Probar formato DD/MM/YYYY
                    dt = datetime.strptime(value, "%d/%m/%Y")
                    operator[internal_key] = int(
                        dt.replace(tzinfo=timezone.utc).timestamp()
                    )
                except ValueError:
                    try:
                        # Probar formato YYYY-MM-DD
                        dt = datetime.strptime(value, "%Y-%m-%d")
                        operator[internal_key] = int(
                            dt.replace(tzinfo=timezone.utc).timestamp()
                        )
                    except ValueError:
                        print(
                            f"Fila {row_num}: Formato de fecha inválido en {internal_key}: {value}"
                        )
                        operator[internal_key] = None
            else:
                operator[internal_key] = None

        elif internal_key == "updated_at":
            # Convertir fecha y hora "HH:MM DD/MM/YYYY" a timestamp
            if value:
                try:
                    # Formato "HH:MM DD/MM/YYYY"
                    dt = datetime.strptime(value, "%H:%M %d/%m/%Y")
                    operator[internal_key] = int(
                        dt.replace(tzinfo=timezone.utc).timestamp()
                    )
                except ValueError:
                    try:
                        # Formato alternativo "YYYY-MM-DD HH:MM:SS"
                        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                        operator[internal_key] = int(
                            dt.replace(tzinfo=timezone.utc).timestamp()
                        )
                    except ValueError:
                        # Si no se puede parsear, usar timestamp actual
                        operator[internal_key] = int(
                            datetime.now(timezone.utc).timestamp()
                        )
            else:
                operator[internal_key] = int(datetime.now(timezone.utc).timestamp())
        else:
            # Campos de texto simples
            operator[internal_key] = value

    # Validar campos obligatorios
    if not operator.get("callsign") or not operator.get("name"):
        print(f"Fila {row_num}: Faltan campos obligatorios")
        return None

    # Establecer valores por defecto
    operator.setdefault("category", "NO_APLICA")
    operator.setdefault("type", "")
    operator.setdefault("region", "")
    operator.setdefault("district", "")
    operator.setdefault("province", "")
    operator.setdefault("department", "")
    operator.setdefault("license", "")
    operator.setdefault("resolution", "")
    operator.setdefault("enabled", 1)
    operator.setdefault("country", "")
    operator.setdefault("expiration_date", None)
    operator.setdefault("cutoff_date", None)
    operator.setdefault("updated_at", int(datetime.now(timezone.utc).timestamp()))

    return operator


def _get_country_code_from_name(country_name: str) -> Optional[str]:
    """
    Busca el código ITU de un país dado su nombre en español o inglés.
    """
    normalized_name = normalize_ascii(country_name.lower().strip())

    for code, names in ITU_COUNTRY_NAMES.items():
        for lang_code, name in names.items():
            if normalize_ascii(name.lower()) == normalized_name:
                return code

    return None
