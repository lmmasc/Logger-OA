from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from ...domain.models import Operation, OperationContact, Contest, ContestContact


def _migrate_operation_es_to_en(data: Dict[str, Any]) -> Dict[str, Any]:
    # If already in EN (has 'type' or 'stations'), return as-is
    if "type" in data or "stations" in data:
        return data
    mapping = {
        "tipo": "type",
        "operador": "operator",
        "banda": "band",
        "frecuencia": "frequency",
        "modo": "mode",
        "repetidor": "repeater",
        "creado_el": "created_at",
        "estaciones": "stations",
        "version_esquema": "schema_version",
    }
    migrated: Dict[str, Any] = {}
    for k, v in data.items():
        migrated[mapping.get(k, k)] = v
    # Migrate stations entries
    stations = []
    for s in migrated.get("stations", []) or []:
        s_map = {
            "indicativo": "callsign",
            "nombre": "name",
            "estacion": "station",
            "energia": "energy",
            "potencia": "power",
            "qtr_oa": "qtr_oa",
            "qtr_utc": "qtr_utc",
            "obs": "obs",
            # rs_rx/rs_tx usually same keys
        }
        s_m = {}
        for k, v in s.items():
            s_m[s_map.get(k, k)] = v
        stations.append(s_m)
    if stations:
        migrated["stations"] = stations
    return migrated


def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


# -------- Serialization helpers ---------


def _operation_to_dict(op: Operation) -> Dict[str, Any]:
    return {
        "type": op.type,
        "operator": op.operator,
        "band": op.band,
        "frequency": op.frequency,
        "mode": op.mode,
        "repeater": op.repeater,
        "created_at": op.created_at,
        "stations": [
            {
                "callsign": s.callsign,
                "name": s.name,
                "station": s.station,
                "energy": s.energy,
                "power": s.power,
                "rs_rx": s.rs_rx,
                "rs_tx": s.rs_tx,
                "qtr_oa": s.qtr_oa,
                "qtr_utc": s.qtr_utc,
                "obs": s.obs,
            }
            for s in op.stations
        ],
        "schema_version": op.schema_version,
    }


def _operation_from_dict(data: Dict[str, Any]) -> Operation:
    # migrate Spanish keys to English if needed
    data = _migrate_operation_es_to_en(data)
    stations = [
        OperationContact(
            callsign=s.get("callsign", ""),
            name=s.get("name", "-"),
            station=s.get("station", "-"),
            energy=s.get("energy", "-"),
            power=s.get("power", "-"),
            rs_rx=s.get("rs_rx", "-"),
            rs_tx=s.get("rs_tx", "-"),
            qtr_oa=s.get("qtr_oa", ""),
            qtr_utc=s.get("qtr_utc", ""),
            obs=s.get("obs", "-"),
        )
        for s in data.get("stations", [])
    ]
    return Operation(
        type=data.get("type", ""),
        operator=data.get("operator", ""),
        band=data.get("band", ""),
        frequency=data.get("frequency", ""),
        mode=data.get("mode", ""),
        repeater=data.get("repeater", ""),
        created_at=data.get("created_at", ""),
        stations=stations,
        schema_version=int(data.get("schema_version", 1)),
    )


def _contest_to_dict(c: Contest) -> Dict[str, Any]:
    return {
        "name": c.name,
        "operator": c.operator,
        "created_at": c.created_at,
        "contacts": [
            {
                "callsign": cc.callsign,
                "name": cc.name,
                "exchange_received": cc.exchange_received,
                "exchange_sent": cc.exchange_sent,
                "block": cc.block,
                "points": cc.points,
                "time_oa": cc.time_oa,
                "time_utc": cc.time_utc,
            }
            for cc in c.contacts
        ],
        "schema_version": c.schema_version,
    }


def _contest_from_dict(data: Dict[str, Any]) -> Contest:
    # migrate Spanish keys to English if needed
    if "contacts" not in data and "contactos" in data:
        mapping = {
            "nombre": "name",
            "operador": "operator",
            "creado_el": "created_at",
            "contactos": "contacts",
            "version_esquema": "schema_version",
        }
        data = {mapping.get(k, k): v for k, v in data.items()}
        migrated_contacts = []
        for cc in data.get("contacts", []) or []:
            c_map = {
                "indicativo": "callsign",
                "nombre": "name",
                "intercambio_recibido": "exchange_received",
                "intercambio_enviado": "exchange_sent",
                "bloque": "block",
                "puntos": "points",
                "hora_oa": "time_oa",
                "hora_utc": "time_utc",
            }
            migrated_contacts.append({c_map.get(k, k): v for k, v in cc.items()})
        data["contacts"] = migrated_contacts
    contacts = [
        ContestContact(
            callsign=cc.get("callsign", ""),
            name=cc.get("name", "-"),
            exchange_received=cc.get("exchange_received", "-"),
            exchange_sent=cc.get("exchange_sent", "-"),
            block=int(cc.get("block", 1)),
            points=int(cc.get("points", 0)),
            time_oa=cc.get("time_oa", ""),
            time_utc=cc.get("time_utc", ""),
        )
        for cc in data.get("contacts", [])
    ]
    return Contest(
        name=data.get("name", ""),
        operator=data.get("operator", ""),
        created_at=data.get("created_at", ""),
        contacts=contacts,
        schema_version=int(data.get("schema_version", 1)),
    )


# ---------- Repositories -------------


class JsonOperationsRepo:
    def save(self, op: Operation, path: str) -> None:
        _ensure_parent(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(_operation_to_dict(op), f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> Operation:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _operation_from_dict(data)


class JsonContestsRepo:
    def save(self, c: Contest, path: str) -> None:
        _ensure_parent(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(_contest_to_dict(c), f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> Contest:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _contest_from_dict(data)
