from __future__ import annotations

from typing import Callable, Iterable, Dict
from dataclasses import dataclass
from ...domain.models import RadioOperator
from ..repositories.radio_operators import IRadioOperatorsRepo
from ...utils.dates import parse_ddmmyyyy
from ...utils.text import normalize_callsign
from app.operators_update.updater import update_operators_from_pdf


@dataclass
class ImportResult:
    total_upserts: int
    created: int
    updated: int
    reenabled: int
    disabled_oa: int


class ImportService:
    def __init__(self, repo: IRadioOperatorsRepo):
        self.repo = repo

    def import_radio_operators(
        self,
        rows: Iterable[dict],
        cutoff_date: str,
        progress_cb: Callable[[int, int, str], None] | None = None,
    ) -> ImportResult:
        # 1) Agrupar y normalizar: por cada indicativo, conservar el de mayor vencimiento
        parse_ddmmyyyy(cutoff_date)  # valida formato
        new_map: Dict[str, RadioOperator] = {}
        for idx, r in enumerate(rows, start=1):
            cs = normalize_callsign(str(r.get("callsign", "")).upper())
            if not cs:
                continue
            ro = RadioOperator(
                callsign=cs,
                name=r.get("name", ""),
                category=r.get("category", ""),
                type=r.get("type", ""),
                district=r.get("district", ""),
                province=r.get("province", ""),
                department=r.get("department", ""),
                license=r.get("license", ""),
                resolution=r.get("resolution", ""),
                expiration_date=r.get("expiration_date", ""),
                enabled=1,
                country=r.get("country", "Peru"),
                updated_at=r.get("updated_at", ""),
            )
            prev = new_map.get(ro.callsign)
            if prev is None:
                new_map[ro.callsign] = ro
            else:
                d1 = parse_ddmmyyyy(prev.expiration_date)
                d2 = parse_ddmmyyyy(ro.expiration_date)
                if d2 and (not d1 or d2 > d1):
                    new_map[ro.callsign] = ro
            if progress_cb and idx % 50 == 0:
                progress_cb(idx, -1, "parse")

        # 2) Fusionar con BD: habilitar los presentes; actualizar si traen mayor vencimiento
        existing_list = self.repo.list_all()
        existing: Dict[str, RadioOperator] = {x.callsign: x for x in existing_list}

        to_upsert: list[RadioOperator] = []
        created = 0
        updated = 0
        reenabled = 0

        for cs, incoming in new_map.items():
            cur = existing.get(cs)
            if cur is None:
                incoming.enabled = 1
                to_upsert.append(incoming)
                created += 1
            else:
                d_cur = parse_ddmmyyyy(cur.expiration_date)
                d_inc = parse_ddmmyyyy(incoming.expiration_date)
                if d_inc and (not d_cur or d_inc > d_cur):
                    incoming.enabled = 1
                    to_upsert.append(incoming)
                    updated += 1
                else:
                    if cur.enabled != 1:
                        cur.enabled = 1
                        to_upsert.append(cur)
                        reenabled += 1

        # 3) Deshabilitar OA ausentes en el nuevo PDF
        incoming_set = set(new_map.keys())
        disabled_oa = 0
        for cs, cur in existing.items():
            if not cs.upper().startswith("OA"):
                continue
            if cs not in incoming_set and cur.enabled != 0:
                cur.enabled = 0
                to_upsert.append(cur)
                disabled_oa += 1

        if to_upsert:
            self.repo.upsert_many(to_upsert)
        return ImportResult(
            total_upserts=len(to_upsert),
            created=created,
            updated=updated,
            reenabled=reenabled,
            disabled_oa=disabled_oa,
        )


"""
Servicio para importar operadores desde un archivo PDF.
Extrae la lógica de negocio fuera de la UI principal.
"""


def import_operators_from_pdf(file_path: str) -> bool:
    """
    Importa operadores desde un archivo PDF usando el updater correspondiente.
    Args:
        file_path (str): Ruta al archivo PDF.
    Returns:
        bool: True si la importación fue exitosa, False en caso contrario.
    """
    return update_operators_from_pdf(file_path)
