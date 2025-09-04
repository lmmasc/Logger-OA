from dataclasses import dataclass, field
from typing import List, Optional
from .operation_contact import OperationContact
from .contact_log import ContactLog


@dataclass
class OperationLog(ContactLog):
    type: str = ""
    band: str = ""
    frequency: str = ""
    mode: str = ""
    repeater: str = ""
    schema_version: int = 1
    contacts: List[OperationContact] = field(default_factory=list)
