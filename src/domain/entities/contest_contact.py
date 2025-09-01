from dataclasses import dataclass


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
