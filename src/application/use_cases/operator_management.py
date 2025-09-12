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
