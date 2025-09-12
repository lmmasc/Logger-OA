"""
Controlador para la gestión de operadores de radio.
Actúa como intermediario entre la UI y los servicios/casos de uso.
"""

from application.use_cases.radio_operator_management import RadioOperatorManagement
from infrastructure.repositories.sqlite_radio_operator_repository import (
    SqliteRadioOperatorRepository,
)


class RadioOperatorController:
    def __init__(self):
        repo = SqliteRadioOperatorRepository()
        self.service = RadioOperatorManagement(repo)

    def list_operators(self):
        return self.service.list_operators()

    def delete_operator_by_callsign(self, callsign: str) -> None:
        self.service.delete_operator_by_callsign(callsign)

    def add_operator(self, operator_data: dict) -> None:
        """
        Recibe un dict con los datos del operador (incluyendo region) y lo agrega usando la entidad y el caso de uso.
        """
        from domain.entities.radio_operator import RadioOperator

        operator = RadioOperator(
            callsign=operator_data.get("callsign", ""),
            name=operator_data.get("name", ""),
            category=operator_data.get("category", ""),
            type_=operator_data.get("type", ""),
            region=operator_data.get("region", ""),
            district=operator_data.get("district", ""),
            province=operator_data.get("province", ""),
            department=operator_data.get("department", ""),
            license_=operator_data.get("license", ""),
            resolution=operator_data.get("resolution", ""),
            expiration_date=operator_data.get("expiration_date", ""),
            cutoff_date=operator_data.get("cutoff_date", ""),
            enabled=operator_data.get("enabled", 1),
            country=operator_data.get("country", ""),
            updated_at=operator_data.get("updated_at", None),
        )
        self.service.add_operator(operator)

    def update_operator(self, operator_data: dict) -> None:
        """
        Recibe un dict con los datos del operador (incluyendo region) y lo actualiza usando la entidad y el caso de uso.
        """
        from domain.entities.radio_operator import RadioOperator

        operator = RadioOperator(
            callsign=operator_data.get("callsign", ""),
            name=operator_data.get("name", ""),
            category=operator_data.get("category", ""),
            type_=operator_data.get("type", ""),
            region=operator_data.get("region", ""),
            district=operator_data.get("district", ""),
            province=operator_data.get("province", ""),
            department=operator_data.get("department", ""),
            license_=operator_data.get("license", ""),
            resolution=operator_data.get("resolution", ""),
            expiration_date=operator_data.get("expiration_date", ""),
            cutoff_date=operator_data.get("cutoff_date", ""),
            enabled=operator_data.get("enabled", 1),
            country=operator_data.get("country", ""),
            updated_at=operator_data.get("updated_at", None),
        )
        self.service.update_operator(operator)

    # Métodos adicionales para agregar, actualizar, etc. pueden agregarse aquí
