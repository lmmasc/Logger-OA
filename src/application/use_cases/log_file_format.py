import uuid
from typing import Any, Dict, Tuple

from interface_adapters.ui.view_manager import LogType
from utils.datetime import parse_utc_timestamp


CURRENT_LOG_FILE_FORMAT_VERSION = 2


def _coerce_blank_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    if text in {"", "-", "None", "none", "null", "NULL"}:
        return default
    return text


def normalize_log_metadata(log_type: str, metadata: Dict[str, Any] | None) -> Dict[str, Any]:
    meta = dict(metadata or {})

    if log_type == LogType.OPERATION_LOG.value:
        meta.setdefault("operation_type", meta.get("type", "type"))
        meta.setdefault("frequency_band", meta.get("band", "band"))
        meta.setdefault("mode_key", meta.get("mode", ""))
        meta.setdefault("frequency", meta.get("frequency", ""))
        meta.setdefault("repeater_key", meta.get("repeater", None))
    elif log_type == LogType.CONTEST_LOG.value:
        meta.setdefault("contest_name_key", meta.get("contest_key", "contest"))

    meta["file_format_version"] = CURRENT_LOG_FILE_FORMAT_VERSION
    return meta


def normalize_contact(log_type: str, contact: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(contact or {})
    normalized["id"] = normalized.get("id") or str(uuid.uuid4())
    normalized["callsign"] = _coerce_blank_text(normalized.get("callsign"), "")
    normalized["timestamp"] = parse_utc_timestamp(normalized.get("timestamp"))

    if log_type == LogType.OPERATION_LOG.value:
        defaults = {
            "name": "-",
            "country": "-",
            "region": "-",
            "station": "",
            "energy": "",
            "power": "",
            "rs_rx": "",
            "rs_tx": "",
            "obs": "",
        }
    elif log_type == LogType.CONTEST_LOG.value:
        defaults = {
            "name": "-",
            "region": "-",
            "exchange_received": "",
            "exchange_sent": "",
            "rs_rx": "",
            "rs_tx": "",
            "obs": "",
            "block": 1,
            "points": 0,
        }
    else:
        defaults = {}

    for key, default_value in defaults.items():
        normalized.setdefault(key, default_value)

    text_fields = {
        "callsign": "",
        "name": "-",
        "country": "-",
        "region": "-",
        "station": "",
        "energy": "",
        "power": "",
        "rs_rx": "",
        "rs_tx": "",
        "obs": "",
        "exchange_received": "",
        "exchange_sent": "",
    }
    for key, default_value in text_fields.items():
        if key in normalized:
            normalized[key] = _coerce_blank_text(normalized.get(key), default_value)

    if "block" in normalized:
        try:
            normalized["block"] = int(normalized.get("block", 1) or 1)
        except (TypeError, ValueError):
            normalized["block"] = 1
    if "points" in normalized:
        try:
            normalized["points"] = int(normalized.get("points", 0) or 0)
        except (TypeError, ValueError):
            normalized["points"] = 0

    return normalized


def normalize_log_payload(
    log_type: str,
    start_time: Any,
    end_time: Any,
    metadata: Dict[str, Any] | None,
) -> Tuple[int, int, Dict[str, Any]]:
    return (
        parse_utc_timestamp(start_time),
        parse_utc_timestamp(end_time),
        normalize_log_metadata(log_type, metadata),
    )