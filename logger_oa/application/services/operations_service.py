from __future__ import annotations

from typing import Optional

from ..repositories.operations import IOperationsRepo
from ...domain.models import Operation, OperationContact


class OperationsService:
    def __init__(self, repo: IOperationsRepo):
        self.repo = repo

    def new_operation(
        self,
        type: str,
        operator: str,
        band: str = "",
        mode: str = "",
        created_at: str = "",
    ) -> Operation:
        return Operation(
            type=type, operator=operator, band=band, mode=mode, created_at=created_at
        )

    def add_contact(self, op: Operation, contact: OperationContact) -> None:
        op.stations.append(contact)

    def save(self, op: Operation, path: str) -> None:
        self.repo.save(op, path)

    def load(self, path: str) -> Operation:
        return self.repo.load(path)
