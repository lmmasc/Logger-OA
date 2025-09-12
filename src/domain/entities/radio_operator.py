from dataclasses import dataclass
from typing import Optional


@dataclass
class RadioOperator:
    callsign: str
    name: str
    category: str
    type_: str
    region: str  # Nuevo campo movido después de type_
    district: str
    province: str
    department: str
    license_: str
    resolution: str
    expiration_date: str
    cutoff_date: str
    enabled: int
    country: str
    updated_at: Optional[str] = None
