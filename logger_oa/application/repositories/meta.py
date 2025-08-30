from __future__ import annotations

from typing import Optional, Protocol


class IMetaRepo(Protocol):
    def set(self, key: str, value: str) -> None: ...

    def get(self, key: str) -> Optional[str]: ...
