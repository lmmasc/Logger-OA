"""
Caso de uso: Gestión de operadores de radio.
Incluye listar, agregar, actualizar y deshabilitar operadores.
"""

from typing import List
from domain.entities.radio_operator import RadioOperator
from application.interfaces.radio_operator_repository import RadioOperatorRepository


class RadioOperatorManagement:
    def __init__(self, repository: RadioOperatorRepository):
        self.repository = repository

    def list_operators(self) -> List[RadioOperator]:
        return self.repository.list_all()

    def add_operator(self, operator: RadioOperator) -> None:
        self.repository.add(operator)

    def update_operator(self, operator: RadioOperator) -> None:
        self.repository.update(operator)

    def disable_absent_operators(self, present_callsigns: list[str]) -> None:
        self.repository.disable_absent(present_callsigns)
