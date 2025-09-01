from domain.entities.radio_operator import RadioOperator
from abc import ABC, abstractmethod
from typing import List


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
