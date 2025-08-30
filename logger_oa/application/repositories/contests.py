from __future__ import annotations

from typing import Protocol
from ...domain.models import Contest


class IContestsRepo(Protocol):
    def save(self, c: Contest, path: str) -> None: ...

    def load(self, path: str) -> Contest: ...
