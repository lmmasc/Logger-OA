from typing import List
from domain.entities.radio_operator import RadioOperator
from application.interfaces.radio_operator_repository import RadioOperatorRepository
from app.db import queries


class SqliteRadioOperatorRepository(RadioOperatorRepository):
    def list_all(self) -> List[RadioOperator]:
        rows = queries.get_radio_operators()
        return [RadioOperator(*row) for row in rows]

    def add(self, operator: RadioOperator) -> None:
        queries.add_radio_operator(
            operator.callsign,
            operator.name,
            operator.category,
            operator.type_,
            operator.district,
            operator.province,
            operator.department,
            operator.license_,
            operator.resolution,
            operator.expiration_date,
            operator.cutoff_date,
            operator.enabled,
            operator.country,
            operator.updated_at,
        )

    def update(self, operator: RadioOperator) -> None:
        queries.update_radio_operator(
            operator.callsign,
            operator.name,
            operator.category,
            operator.type_,
            operator.district,
            operator.province,
            operator.department,
            operator.license_,
            operator.resolution,
            operator.expiration_date,
            operator.cutoff_date,
            operator.enabled,
            operator.country,
            operator.updated_at,
        )

    def disable_absent(self, present_callsigns: list[str]) -> None:
        # Implementación pendiente según lógica de negocio
        pass
