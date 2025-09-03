from abc import ABC, abstractmethod
from typing import List
from domain.entities.radio_operator import RadioOperator


class RadioOperatorRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[RadioOperator]:
        pass

    @abstractmethod
    def add(self, operator: RadioOperator) -> None:
        pass

    @abstractmethod
    def update(self, operator: RadioOperator) -> None:
        pass

    @abstractmethod
    def disable_absent(self, present_callsigns: list[str]) -> None:
        pass

    @abstractmethod
    def delete_by_callsign(self, callsign: str) -> None:
        pass
