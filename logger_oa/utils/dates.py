from __future__ import annotations

from datetime import datetime


def parse_ddmmyyyy(date_str: str) -> datetime | None:
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except Exception:
        return None


__all__ = ["parse_ddmmyyyy"]
