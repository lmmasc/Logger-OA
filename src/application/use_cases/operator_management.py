"""
Casos de uso para gestión de operadores (consulta y creación).
"""

from infrastructure.repositories.sqlite_radio_operator_repository import (
    SqliteRadioOperatorRepository,
)
from domain.entities.radio_operator import RadioOperator


def get_operator_by_callsign(callsign: str):
    repo = SqliteRadioOperatorRepository()
    return repo.get_operator_by_callsign(callsign)


def create_operator(op_data: dict):
    # Mapear claves 'type' y 'license' a 'type_' y 'license_'
    if "type" in op_data:
        op_data["type_"] = op_data.pop("type")
    if "license" in op_data:
        op_data["license_"] = op_data.pop("license")
    new_operator = RadioOperator(**op_data)
    repo = SqliteRadioOperatorRepository()
    repo.add(new_operator)
    return new_operator


def find_operator_for_input(callsign: str) -> RadioOperator | None:
    """
    Resuelve el operador a partir del texto ingresado por el usuario, manteniendo la lógica anterior
    de separación de prefijo/base/sufijo pero utilizando consultas SQLite (rápidas):
    1) Busca por base
    2) Si hay prefijo, intenta prefijo/base
    3) Finalmente intenta el texto completo
    """
    from utils.callsign_parser import parse_callsign

    repo = SqliteRadioOperatorRepository()
    cs = (callsign or "").strip().upper()
    base, prefijo, _ = parse_callsign(cs)
    # 1) base
    op = repo.get_operator_by_callsign(base) if base else None
    # 2) prefijo/base
    if not op and prefijo:
        op = repo.get_operator_by_callsign(f"{prefijo}/{base}")
    # 3) texto completo
    if not op and cs:
        op = repo.get_operator_by_callsign(cs)
    return op
