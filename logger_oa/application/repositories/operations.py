from __future__ import annotations

from typing import Protocol
from ...domain.models import Operation


class IOperationsRepo(Protocol):
    def save(self, op: Operation, path: str) -> None: ...

    def load(self, path: str) -> Operation: ...
