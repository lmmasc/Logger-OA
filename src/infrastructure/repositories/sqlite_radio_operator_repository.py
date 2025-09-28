# Archivo migrado desde src/app/repositories/sqlite_radio_operator_repository.py
from typing import List, Tuple, Optional
from domain.entities.radio_operator import RadioOperator
from domain.repositories.radio_operator_repository import RadioOperatorRepository
from infrastructure.db import queries
from dataclasses import dataclass


@dataclass
class OperatorSuggestion:
    callsign: str
    name: str


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

    def get_by_callsign(self, callsign: str) -> Optional[RadioOperator]:
        row = queries.get_radio_operator_by_callsign(callsign)
        if row:
            # Alinear conversión con list_all/list_paged: convertir fechas str a int y vacíos a None
            row_list = list(row)
            for idx in [10, 11, 14]:  # expiration_date, cutoff_date, updated_at
                val = row_list[idx]
                if isinstance(val, str):
                    if val.isdigit():
                        row_list[idx] = int(val)
                    elif val.strip() == "":
                        row_list[idx] = None
            return RadioOperator(*row_list)
        return None

    # Alias por compatibilidad con código existente en UI
    def get_operator_by_callsign(self, callsign: str) -> Optional[RadioOperator]:
        return self.get_by_callsign(callsign)

    def search_suggestions(
        self, prefix: str, limit: int = 50
    ) -> List[OperatorSuggestion]:
        """
        Retorna sugerencias por prefijo usando SQL LIKE, p.ej. 'OA%'.
        """
        pattern = f"{prefix}%"
        rows = queries.search_radio_operators_by_callsign(pattern, limit=limit)
        return [OperatorSuggestion(callsign=r[0], name=r[1] or "") for r in rows]

    def list_paged(
        self,
        page: int,
        page_size: int,
        order_by: str = "callsign",
        asc: bool = True,
        filter_col: Optional[str] = None,
        filter_text: Optional[str] = None,
    ) -> Tuple[List[RadioOperator], int]:
        """Lista paginada y filtrada desde SQLite."""
        # Seguridad básica de columnas permitidas
        allowed_cols = {
            "callsign",
            "name",
            "category",
            "type",
            "region",
            "district",
            "province",
            "department",
            "license",
            "resolution",
            "expiration_date",
            "cutoff_date",
            "enabled",
            "country",
            "updated_at",
        }
        if order_by not in allowed_cols:
            order_by = "callsign"
        rows, total = queries.get_radio_operators_paged(
            page=page,
            page_size=page_size,
            order_by=order_by,
            asc=asc,
            filter_col=filter_col if filter_col in allowed_cols else None,
            filter_text=filter_text,
        )
        result = []
        for row in rows:
            row = list(row)
            for idx in [10, 11, 14]:
                val = row[idx]
                if isinstance(val, str):
                    if val.isdigit():
                        row[idx] = int(val)
                    elif val.strip() == "":
                        row[idx] = None
            result.append(RadioOperator(*row))
        return result, total
