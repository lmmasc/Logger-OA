"""
Caso de uso: Gestión de operadores de radio.
Incluye listar, agregar, actualizar y deshabilitar operadores.
"""

from typing import List, Tuple, Optional
from domain.entities.radio_operator import RadioOperator
from domain.repositories.radio_operator_repository import RadioOperatorRepository


class RadioOperatorManagement:
    def __init__(self, repository: RadioOperatorRepository):
        self.repository = repository

    def list_operators(self) -> List[RadioOperator]:
        return self.repository.list_all()

    def list_operators_paged(
        self,
        page: int,
        page_size: int,
        order_by: str = "callsign",
        asc: bool = True,
        filter_col: str | None = None,
        filter_text: str | None = None,
    ) -> Tuple[List[RadioOperator], int]:
        return self.repository.list_paged(
            page=page,
            page_size=page_size,
            order_by=order_by,
            asc=asc,
            filter_col=filter_col,
            filter_text=filter_text,
        )

    def add_operator(self, operator: RadioOperator) -> None:
        self.repository.add(operator)

    def update_operator(self, operator: RadioOperator) -> None:
        self.repository.update(operator)

    def disable_absent_operators(self, present_callsigns: list[str]) -> None:
        self.repository.disable_absent(present_callsigns)

    def delete_operator_by_callsign(self, callsign: str) -> None:
        self.repository.delete_by_callsign(callsign)

    def get_operator_by_callsign(self, callsign: str) -> Optional[RadioOperator]:
        return self.repository.get_by_callsign(callsign)
