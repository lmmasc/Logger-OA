from dataclasses import dataclass


@dataclass
class ContestContact:
    id: str
    callsign: str
    name: str = "-"
    region: str = "-"
    exchange_received: str = "-"
    exchange_sent: str = "-"
    rs_rx: str = "-"
    rs_tx: str = "-"
    obs: str = ""
    block: int = 1
    points: int = 0
    timestamp: int = 0
