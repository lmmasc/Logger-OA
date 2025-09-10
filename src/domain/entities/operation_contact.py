from dataclasses import dataclass


@dataclass
class OperationContact:
    callsign: str
    id: str = ""
    name: str = "-"
    country: str = "-"
    station: str = "-"
    energy: str = "-"
    power: str = "-"
    rs_rx: str = "-"
    rs_tx: str = "-"
    timestamp: int = 0
    obs: str = "-"
