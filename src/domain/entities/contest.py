from dataclasses import dataclass, field
from typing import List
from .contest_contact import ContestContact


@dataclass
class Contest:
    name: str
    operator: str
    created_at: str = ""
    contacts: List[ContestContact] = field(default_factory=list)
    schema_version: int = 1
