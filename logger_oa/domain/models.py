from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RadioOperator:
    callsign: str
    name: str = ""
    category: str = ""
    type: str = ""
    district: str = ""
    province: str = ""
    department: str = ""
    license: str = ""
    resolution: str = ""
    expiration_date: str = ""  # dd/mm/yyyy
    enabled: int = 1  # 1/0 to match SQLite schema easily
    country: str = ""
    updated_at: str = ""  # ISO-like string or label (e.g., 'manual')


@dataclass
class OperationContact:
    callsign: str
    name: str = "-"
    station: str = "-"
    energy: str = "-"
    power: str = "-"
    rs_rx: str = "-"
    rs_tx: str = "-"
    qtr_oa: str = ""
    qtr_utc: str = ""
    obs: str = "-"


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


@dataclass
class ContestContact:
    callsign: str
    name: str = "-"
    exchange_received: str = "-"
    exchange_sent: str = "-"
    block: int = 1
    points: int = 0
    time_oa: str = ""
    time_utc: str = ""


@dataclass
class Contest:
    name: str
    operator: str
    created_at: str = ""
    contacts: List[ContestContact] = field(default_factory=list)
    schema_version: int = 1


__all__ = [
    "RadioOperator",
    "OperationContact",
    "Operation",
    "ContestContact",
    "Contest",
]
