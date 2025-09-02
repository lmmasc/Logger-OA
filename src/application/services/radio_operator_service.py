from typing import List
from domain.entities.radio_operator import RadioOperator
from domain.repositories.radio_operator_repository import RadioOperatorRepository


class RadioOperatorService:
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
