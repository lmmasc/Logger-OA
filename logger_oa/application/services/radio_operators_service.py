from __future__ import annotations

from typing import List
from ...domain.models import RadioOperator
from ..repositories.radio_operators import IRadioOperatorsRepo


class RadioOperatorsService:
    def __init__(self, repo: IRadioOperatorsRepo):
        self.repo = repo

    def list(
        self, filter_text: str | None = None, field: str = "callsign"
    ) -> List[RadioOperator]:
        items = self.repo.list_all()
        if not filter_text:
            return items
        ft = (filter_text or "").lower()
        return [x for x in items if ft in str(getattr(x, field, "")).lower()]

    def upsert(self, item: RadioOperator) -> None:
        self.repo.upsert_one(item)

    def delete(self, callsign: str) -> None:
        self.repo.delete_by_callsign(callsign)
