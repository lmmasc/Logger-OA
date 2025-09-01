from dataclasses import dataclass, field
from typing import List
from .operation_contact import OperationContact


@dataclass
class Operation:
    type: str
    operator: str
    band: str = ""
    frequency: str = ""
    mode: str = ""
    repeater: str = ""
    created_at: str = ""
    stations: List[OperationContact] = field(default_factory=list)
    schema_version: int = 1
