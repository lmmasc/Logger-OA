from dataclasses import dataclass


@dataclass
class ContestContact:
    callsign: str
    name: str = "-"
    region: str = "-"
    exchange_received: str = "-"
    exchange_sent: str = "-"
    rs_rx: str = "-"
    rs_tx: str = "-"
    observations: str = ""
    block: int = 1
    points: int = 0
    time_oa: str = ""
    time_utc: str = ""
