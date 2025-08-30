from __future__ import annotations

from typing import Optional

from ..repositories.contests import IContestsRepo
from ...domain.models import Contest, ContestContact


class ContestsService:
    def __init__(self, repo: IContestsRepo):
        self.repo = repo

    def new_contest(self, name: str, operator: str, created_at: str = "") -> Contest:
        return Contest(name=name, operator=operator, created_at=created_at)

    def add_contact(self, c: Contest, contact: ContestContact) -> None:
        c.contacts.append(contact)

    def save(self, c: Contest, path: str) -> None:
        self.repo.save(c, path)

    def load(self, path: str) -> Contest:
        return self.repo.load(path)
