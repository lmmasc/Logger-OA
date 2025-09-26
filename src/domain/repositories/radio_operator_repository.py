from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
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

    @abstractmethod
    def get_by_callsign(self, callsign: str) -> Optional[RadioOperator]:
        """Obtiene un operador por su indicativo exacto."""
        pass

    @abstractmethod
    def list_paged(
        self,
        page: int,
        page_size: int,
        order_by: str = "callsign",
        asc: bool = True,
        filter_col: Optional[str] = None,
        filter_text: Optional[str] = None,
    ) -> Tuple[List[RadioOperator], int]:
        """Lista paginada con total, opcionalmente filtrada por columna (LIKE)."""
        pass
