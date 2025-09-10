from dataclasses import dataclass


@dataclass
class OperationContact:
    callsign: str
    name: str = "-"
    country: str = "-"
    station: str = "-"
    energy: str = "-"
    power: str = "-"
    rs_rx: str = "-"
    rs_tx: str = "-"
    qtr_oa: str = ""
    qtr_utc: str = ""
    obs: str = "-"
