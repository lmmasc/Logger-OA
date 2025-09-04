from dataclasses import dataclass, field
from typing import List, Optional
from .contest_contact import ContestContact
from .contact_log import ContactLog


@dataclass
class ContestLog(ContactLog):
    name: str = ""
    schema_version: int = 1
    contacts: List[ContestContact] = field(default_factory=list)
