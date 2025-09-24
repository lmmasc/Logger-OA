# Archivo migrado desde src/app/repositories/sqlite_radio_operator_repository.py
from typing import List
from domain.entities.radio_operator import RadioOperator
from domain.repositories.radio_operator_repository import RadioOperatorRepository
from infrastructure.db import queries


class SqliteRadioOperatorRepository(RadioOperatorRepository):
    def list_all(self) -> List[RadioOperator]:
        rows = queries.get_radio_operators()
        result = []
        for row in rows:
            # Convertir fechas a int si son str numéricos, o None si vacío
            row = list(row)
            for idx in [10, 11, 14]:  # expiration_date, cutoff_date, updated_at
                val = row[idx]
                if isinstance(val, str):
                    if val.isdigit():
                        row[idx] = int(val)
                    elif val.strip() == "":
                        row[idx] = None
            result.append(RadioOperator(*row))
        # Ordenar alfabéticamente por indicativo (callsign)
        result.sort(key=lambda op: op.callsign)
        return result

    def add(self, operator: RadioOperator) -> None:
        queries.add_radio_operator(
            operator.callsign,
            operator.name,
            operator.category,
            operator.type_,
            operator.region,  # Campo region agregado
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
            operator.region,  # Campo region agregado
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

    def delete_by_callsign(self, callsign: str) -> None:
        queries.delete_radio_operator_by_callsign(callsign)

    def get_operator_by_callsign(self, callsign: str):
        from infrastructure.db.queries import get_radio_operator_by_callsign

        row = get_radio_operator_by_callsign(callsign)
        if row:
            from domain.entities.radio_operator import RadioOperator

            return RadioOperator(*row)
        return None
