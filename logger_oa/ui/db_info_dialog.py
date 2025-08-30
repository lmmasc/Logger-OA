from __future__ import annotations

import os
import shutil
import csv
from typing import List
import sqlite3

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from ..infrastructure.db.sqlite_repo import (
    SqliteRadioOperatorsRepo,
    SqliteMetaRepo,
)
from ..application.services.radio_operators_service import RadioOperatorsService
from ..domain.models import RadioOperator
from ..utils.paths import get_database_path


def _human_size(nbytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if nbytes < 1024.0:
            return f"{nbytes:3.1f} {unit}"
        nbytes /= 1024.0
    return f"{nbytes:.1f} PB"


class DatabaseInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Información de la base de datos")
        self.resize(700, 300)

        # Services
        self.repo = SqliteRadioOperatorsRepo()
        self.repo.init_schema()
        self.meta = SqliteMetaRepo()
        self.service = RadioOperatorsService(self.repo)

        # Labels
        self.lbl_path = QLabel("-", self)
        self.lbl_size = QLabel("-", self)
        self.lbl_counts = QLabel("-", self)
        self.lbl_last_pdf = QLabel("-", self)

        # Layout
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Ruta DB:"))
        lay.addWidget(self.lbl_path)
        lay.addWidget(QLabel("Tamaño DB:"))
        lay.addWidget(self.lbl_size)
        lay.addWidget(QLabel("Registros (habilitados/total):"))
        lay.addWidget(self.lbl_counts)
        lay.addWidget(QLabel("Última fecha de PDF:"))
        lay.addWidget(self.lbl_last_pdf)

        # Buttons
        btns = QHBoxLayout()
        self.btn_refresh = QPushButton("Refrescar", self)
        self.btn_backup = QPushButton("Backup DB…", self)
        self.btn_export = QPushButton("Exportar operadores (CSV)…", self)
        self.btn_compact = QPushButton("Compactar DB (VACUUM)…", self)
        self.btn_optimize = QPushButton("Optimizar índices", self)
        self.btn_close = QPushButton("Cerrar", self)
        btns.addWidget(self.btn_refresh)
        btns.addWidget(self.btn_backup)
        btns.addWidget(self.btn_compact)
        btns.addWidget(self.btn_optimize)
        btns.addWidget(self.btn_export)
        btns.addStretch(1)
        btns.addWidget(self.btn_close)
        lay.addLayout(btns)

        # Signals
        self.btn_refresh.clicked.connect(self._refresh)
        self.btn_backup.clicked.connect(self._on_backup)
        self.btn_export.clicked.connect(self._on_export)
        self.btn_compact.clicked.connect(self._on_compact)
        self.btn_optimize.clicked.connect(self._on_optimize)
        self.btn_close.clicked.connect(self.accept)

        self._refresh()

    def _refresh(self):
        try:
            db_path = get_database_path()
            self.lbl_path.setText(db_path)
            try:
                size = os.path.getsize(db_path)
                self.lbl_size.setText(_human_size(float(size)))
            except Exception:
                self.lbl_size.setText("-")
            items: List[RadioOperator] = self.service.list(None, "callsign")
            total = len(items)
            enabled = sum(1 for x in items if getattr(x, "enabled", 1))
            self.lbl_counts.setText(f"{enabled} / {total}")
            last_pdf = self.meta.get("last_pdf_date") or "-"
            self.lbl_last_pdf.setText(str(last_pdf))
        except Exception as e:
            QMessageBox.critical(self, "Información de la base", f"Error: {e}")

    def _on_backup(self):
        src = get_database_path()
        default = os.path.expanduser("~/db_logger_oa.sqlite")
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar copia de DB…", default, "SQLite (*.sqlite *.db)"
        )
        if not path:
            return
        try:
            shutil.copy2(src, path)
            QMessageBox.information(self, "Backup", f"Copia creada: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Backup", f"Error al copiar: {e}")

    def _on_export(self):
        default = os.path.expanduser("~/operadores_radio.csv")
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar operadores…", default, "CSV (*.csv)"
        )
        if not path:
            return
        try:
            items = sorted(
                self.service.list(None, "callsign"), key=lambda x: x.callsign or ""
            )
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(
                    [
                        "Callsign",
                        "Nombre",
                        "Categoría",
                        "Tipo",
                        "Distrito",
                        "Provincia",
                        "Departamento",
                        "Licencia",
                        "Resolución",
                        "Vencimiento",
                        "Habilitado",
                    ]
                )
                for it in items:
                    w.writerow(
                        [
                            it.callsign,
                            it.name,
                            it.category,
                            it.type,
                            it.district,
                            it.province,
                            it.department,
                            it.license,
                            it.resolution,
                            it.expiration_date,
                            "SI" if it.enabled else "NO",
                        ]
                    )
            QMessageBox.information(self, "Exportar", f"Exportado: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Exportar", f"Error al exportar: {e}")

    def _on_compact(self):
        db_path = get_database_path()
        ret = QMessageBox.question(
            self,
            "Compactar DB",
            (
                "Se reconstruirá el archivo de la base (VACUUM).\n"
                "Puede tardar y requiere espacio temporal adicional.\n\n"
                f"¿Continuar con: {db_path}?"
            ),
        )
        if ret != QMessageBox.StandardButton.Yes:
            return
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("VACUUM")
                conn.execute("PRAGMA optimize")
            QMessageBox.information(self, "Compactar DB", "Compactación completada.")
            self._refresh()
        except Exception as e:
            QMessageBox.critical(self, "Compactar DB", f"Error: {e}")

    def _on_optimize(self):
        db_path = get_database_path()
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("PRAGMA optimize")
            QMessageBox.information(self, "Optimizar", "Índices optimizados.")
        except Exception as e:
            QMessageBox.critical(self, "Optimizar", f"Error: {e}")
