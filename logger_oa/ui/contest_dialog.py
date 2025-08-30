from __future__ import annotations

import csv
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import QSettings
from PySide6.QtGui import QKeySequence, QShortcut

from ..application.services.contests_service import ContestsService
from ..infrastructure.files.json_repo import JsonContestsRepo
from ..domain.models import Contest, ContestContact


class ContestDialog(QDialog):
    def __init__(self, parent=None, contest: Contest | None = None):
        super().__init__(parent)
        self.setWindowTitle("Concurso[*]")
        self.resize(900, 600)
        # state
        self._dirty = False
        self._loading = True
        self.setWindowModified(False)

        self.repo = JsonContestsRepo()
        self.svc = ContestsService(self.repo)
        self.contest = (
            contest
            if contest is not None
            else self.svc.new_contest(name="", operator="")
        )

        # Header form
        self.ed_name = QLineEdit(self)
        self.ed_operator = QLineEdit(self)
        header = QHBoxLayout()
        header.addWidget(QLabel("Nombre:"))
        header.addWidget(self.ed_name, 2)
        header.addWidget(QLabel("Operador:"))
        header.addWidget(self.ed_operator, 1)

        # Contacts table (minimal)
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "Callsign",
                "Nombre",
                "Intercambio Rec.",
                "Intercambio Env.",
                "Hora OA",
                "Hora UTC",
                "Bloque",
                "Puntos",
            ]
        )

        # Buttons
        btns = QHBoxLayout()
        self.btn_add = QPushButton("Añadir contacto", self)
        self.btn_calc = QPushButton("Calcular bloque/puntos", self)
        self.btn_save = QPushButton("Guardar…", self)
        self.btn_export = QPushButton("Exportar CSV…", self)
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_calc)
        btns.addStretch(1)
        btns.addWidget(self.btn_export)
        btns.addWidget(self.btn_save)

        lay = QVBoxLayout(self)
        lay.addLayout(header)
        lay.addWidget(self.table, 1)
        lay.addLayout(btns)

        self.btn_add.clicked.connect(self._on_add_contact)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_export.clicked.connect(self._on_export_csv)
        self.btn_calc.clicked.connect(self._on_calc)
        # shortcuts
        QShortcut(QKeySequence.Save, self, self._on_save)

        # tab order / focus
        try:
            self.setTabOrder(self.ed_name, self.ed_operator)
            self.setTabOrder(self.ed_operator, self.table)
        except Exception:
            pass

        # If loaded contest provided, reflect header
        if self.contest:
            self.ed_name.setText(self.contest.name or "")
            self.ed_operator.setText(self.contest.operator or "")

        self._restore_state()
        self._refresh()
        self._loading = False
        self._wire_dirty_signals()

    def _refresh(self):
        self._loading = True
        try:
            self.table.blockSignals(True)
            self.table.setRowCount(len(self.contest.contacts))
            for row, c in enumerate(self.contest.contacts):
                self.table.setItem(row, 0, QTableWidgetItem(c.callsign))
                self.table.setItem(row, 1, QTableWidgetItem(c.name))
                self.table.setItem(row, 2, QTableWidgetItem(c.exchange_received))
                self.table.setItem(row, 3, QTableWidgetItem(c.exchange_sent))
                self.table.setItem(row, 4, QTableWidgetItem(c.time_oa))
                self.table.setItem(row, 5, QTableWidgetItem(c.time_utc))
                self.table.setItem(row, 6, QTableWidgetItem(str(c.block)))
                self.table.setItem(row, 7, QTableWidgetItem(str(c.points)))
        finally:
            self.table.blockSignals(False)
            self._loading = False

    def _on_add_contact(self):
        c = ContestContact(
            callsign="",
            name="-",
            exchange_received="-",
            exchange_sent="-",
            block=1,
            points=0,
        )
        self.svc.add_contact(self.contest, c)
        self._refresh()
        self._mark_dirty()
        # focus first cell of the new row
        try:
            row = max(0, self.table.rowCount() - 1)
            self.table.setCurrentCell(row, 0)
            self.table.editItem(self.table.item(row, 0))
        except Exception:
            pass

    def _on_save(self) -> bool:
        self._sync_from_table()
        # validate times before saving
        invalid_rows = []
        for idx, c in enumerate(self.contest.contacts):
            if c.time_oa:
                hh, mm = self._parse_hhmm(c.time_oa)
                if hh is None:
                    invalid_rows.append(idx + 1)
            if c.time_utc:
                hh, mm = self._parse_hhmm(c.time_utc)
                if hh is None:
                    invalid_rows.append(idx + 1)
        if invalid_rows:
            first = ", ".join(map(str, invalid_rows[:5])) + (
                "…" if len(invalid_rows) > 5 else ""
            )
            ret = QMessageBox.question(
                self,
                "Tiempos inválidos",
                (
                    f"Se encontraron tiempos inválidos en filas: {first}.\n"
                    "¿Deseas guardar de todas formas?"
                ),
            )
            if ret != QMessageBox.StandardButton.Yes:
                return False
        # update contest header
        self.contest.name = self.ed_name.text()
        self.contest.operator = self.ed_operator.text()
        if not (self.contest.name or "").strip():
            QMessageBox.warning(self, "Concurso", "Completa el nombre del concurso.")
            return False
        if not (self.contest.operator or "").strip():
            QMessageBox.warning(self, "Concurso", "Completa el operador.")
            return False

        settings = QSettings("LoggerOA", "ContestDialog")
        last_dir = settings.value("last_dir") or ""
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar concurso…", last_dir, "Concurso (*.json)"
        )
        if not path:
            return False
        # confirm overwrite
        import os

        if os.path.exists(path):
            ret = QMessageBox.question(
                self,
                "Sobrescribir",
                f"El archivo ya existe:\n{path}\n\n¿Deseas sobrescribirlo?",
            )
            if ret != QMessageBox.StandardButton.Yes:
                return False
        settings.setValue("last_dir", path)
        try:
            self.svc.save(self.contest, path)
            QMessageBox.information(self, "Concurso", f"Guardado en: {path}")
            self._dirty = False
            self.setWindowModified(False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Concurso", f"Error al guardar: {e}")
            return False

    def _on_export_csv(self):
        self._sync_from_table()
        settings = QSettings("LoggerOA", "ContestDialog")
        last_dir = settings.value("last_dir") or ""
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar contactos…", last_dir, "CSV (*.csv)"
        )
        if not path:
            return
        settings.setValue("last_dir", path)
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(
                    [
                        "Callsign",
                        "Nombre",
                        "Intercambio Rec.",
                        "Intercambio Env.",
                        "Hora OA",
                        "Hora UTC",
                        "Bloque",
                        "Puntos",
                    ]
                )
                for c in self.contest.contacts:
                    w.writerow(
                        [
                            c.callsign,
                            c.name,
                            c.exchange_received,
                            c.exchange_sent,
                            c.time_oa,
                            c.time_utc,
                            c.block,
                            c.points,
                        ]
                    )
            QMessageBox.information(self, "Exportar CSV", f"Exportado: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Exportar CSV", f"Error al exportar: {e}")

    def _on_calc(self):
        # Placeholder calculation: compute block in decaminute buckets from UTC, points=1 if callsign present
        self._sync_from_table()
        for c in self.contest.contacts:
            hh, mm = self._parse_hhmm(c.time_utc or c.time_oa)
            if hh is None:
                continue
            block = hh * 6 + (mm // 10) + 1
            c.block = int(block)
            c.points = 1 if (c.callsign or "").strip() else 0
        self._refresh()

    def _parse_hhmm(self, s: str | None):
        if not s:
            return (None, None)
        txt = (s or "").strip()
        # Accept HH:MM or HHMM
        if ":" in txt:
            parts = txt.split(":")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                return (max(0, min(23, int(parts[0]))), max(0, min(59, int(parts[1]))))
        elif txt.isdigit() and len(txt) in (3, 4):
            if len(txt) == 3:
                hh = int(txt[0])
                mm = int(txt[1:])
            else:
                hh = int(txt[:2])
                mm = int(txt[2:])
            return (max(0, min(23, hh)), max(0, min(59, mm)))
        return (None, None)

    def _sync_from_table(self):
        # Push current table edits to the underlying model before actions
        for row, c in enumerate(self.contest.contacts):

            def _val(col):
                it = self.table.item(row, col)
                return it.text() if it else ""

            c.callsign = _val(0)
            c.name = _val(1)
            c.exchange_received = _val(2)
            c.exchange_sent = _val(3)
            c.time_oa = _val(4)
            c.time_utc = _val(5)
            try:
                c.block = int(_val(6) or 0)
            except Exception:
                pass
            try:
                c.points = int(_val(7) or 0)
            except Exception:
                pass

    def closeEvent(self, event):
        # prompt on unsaved changes
        if self._dirty:
            m = QMessageBox(self)
            m.setWindowTitle("Cambios sin guardar")
            m.setText("Tienes cambios sin guardar. ¿Deseas guardar antes de cerrar?")
            m.setIcon(QMessageBox.Icon.Warning)
            m.setStandardButtons(
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel
            )
            choice = m.exec()
            if choice == QMessageBox.StandardButton.Save:
                if not self._on_save():
                    event.ignore()
                    return
            elif choice == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            # Discard falls through
        try:
            self._save_state()
        finally:
            super().closeEvent(event)

    def _save_state(self):
        settings = QSettings("LoggerOA", "ContestDialog")
        settings.setValue("name", self.ed_name.text())
        settings.setValue("operator", self.ed_operator.text())

    def _restore_state(self):
        settings = QSettings("LoggerOA", "ContestDialog")
        self.ed_name.setText(settings.value("name") or "")
        self.ed_operator.setText(settings.value("operator") or "")

    def _wire_dirty_signals(self):
        self.ed_name.textChanged.connect(self._mark_dirty)
        self.ed_operator.textChanged.connect(self._mark_dirty)
        self.table.itemChanged.connect(self._on_table_item_changed)

    def _on_table_item_changed(self, *args):
        self._mark_dirty()

    def _mark_dirty(self, *args):
        if self._loading:
            return
        self._dirty = True
        self.setWindowModified(True)
