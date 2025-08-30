from __future__ import annotations

from typing import Callable

from .import_service import ImportService, ImportResult
from ..repositories.meta import IMetaRepo
from ...infrastructure.pdf.radio_operators_parser import extract_radio_operators_rows


class PdfImportOrchestrator:
    def __init__(
        self,
        import_service: ImportService,
        meta_repo: IMetaRepo | None = None,
        parser_func=None,
    ):
        self.import_service = import_service
        self.meta_repo = meta_repo
        self._parser = parser_func or extract_radio_operators_rows

    def import_radio_operators_from_pdf(
        self,
        pdf_path: str,
        cutoff_date: str,
        parse_progress: Callable[[int, int], None] | None = None,
        import_progress: Callable[[int, int, str], None] | None = None,
    ) -> ImportResult:
        rows = self._parser(pdf_path, progress_cb=parse_progress)
        # Extract a cutoff date from rows if present
        cutoff_date = ""
        for r in rows:
            if r.get("cutoff_date"):
                cutoff_date = r["cutoff_date"]
                break
        result = self.import_service.import_radio_operators(
            rows, cutoff_date=cutoff_date, progress_cb=import_progress
        )
        # Save last_pdf_date into meta if available
        if cutoff_date and self.meta_repo is not None:
            self.meta_repo.set("last_pdf_date", cutoff_date)
        return result
