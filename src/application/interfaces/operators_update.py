from abc import ABC, abstractmethod


class OperatorsUpdater(ABC):
    @abstractmethod
    def update_operators_from_pdf(self, file_path: str) -> bool:
        pass
