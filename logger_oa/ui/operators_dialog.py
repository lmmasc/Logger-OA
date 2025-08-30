from __future__ import annotations

from typing import List
import csv
import os

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
    QHeaderView,
    QCheckBox,
)
from PySide6.QtCore import QSettings, Qt

from ..application.services.radio_operators_service import RadioOperatorsService
from ..infrastructure.db.sqlite_repo import SqliteRadioOperatorsRepo, SqliteMetaRepo
from ..domain.models import RadioOperator


class RadioOperatorsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operadores de Radio")
        self.resize(1000, 600)

        # Services
        self.repo = SqliteRadioOperatorsRepo()
        self.repo.init_schema()
        self.service = RadioOperatorsService(self.repo)
        self.meta_repo = SqliteMetaRepo()

        # Controls
        self.filter_edit = QLineEdit(self)
        self.filter_edit.setPlaceholderText("Filtrar…")
        self.field_combo = QComboBox(self)
        self.field_combo.addItems(
            [
                "callsign",
                "name",
                "district",
                "province",
                "department",
                "category",
            ]
        )
        self.refresh_btn = QPushButton("Refrescar", self)
        self.export_btn = QPushButton("Exportar CSV", self)
        self.count_label = QLabel("0 registros", self)
        self.show_disabled_chk = QCheckBox("Mostrar deshabilitados (0)", self)
        self.meta_label = QLabel("Fecha PDF: -", self)

        # Top bar
        top = QHBoxLayout()
        top.addWidget(QLabel("Campo:", self))
        top.addWidget(self.field_combo)
        top.addWidget(self.filter_edit, 1)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.show_disabled_chk)
        top.addWidget(self.export_btn)
        top.addWidget(self.meta_label)
        top.addWidget(self.count_label)

        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
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
        self.table.setSortingEnabled(True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        # Layout
        lay = QVBoxLayout(self)
        lay.addLayout(top)
        lay.addWidget(self.table, 1)

        # Signals
        self.refresh_btn.clicked.connect(self.load_data)
        self.export_btn.clicked.connect(self.export_csv)
        self.filter_edit.textChanged.connect(self.load_data)
        self.field_combo.currentIndexChanged.connect(self.load_data)
        self.show_disabled_chk.toggled.connect(self.load_data)

        # State & initial load
        self._last_items: List[RadioOperator] = []
        self._restore_state()
        self.load_data()

    def load_data(self):
        # Update disabled count label
        full = self.service.list(None, "callsign")
        disabled_count = sum(1 for x in full if not getattr(x, "enabled", 1))
        self.show_disabled_chk.setText(f"Mostrar deshabilitados ({disabled_count})")

        field = self.field_combo.currentText()
        text = self.filter_edit.text()
        items = self.service.list(text, field)
        if not self.show_disabled_chk.isChecked():
            items = [x for x in items if getattr(x, "enabled", 1)]
        self._last_items = items
        self._populate_table(items)
        self.count_label.setText(
            f"{len(items)} registros ({disabled_count} deshabilitados)"
        )
        # Update last PDF date label
        try:
            last_date = self.meta_repo.get("last_pdf_date")
        except Exception:
            last_date = None
        self.meta_label.setText(f"Fecha PDF: {last_date if last_date else '-'}")

    def _populate_table(self, items: List[RadioOperator]):
        # Temporarily disable sorting while populating to avoid flicker
        prev_sort = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(items))
        for row, it in enumerate(items):
            values = [
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
                "Sí" if it.enabled else "No",
            ]
            for col, val in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))
        # Restore sorting and resize to contents
        self.table.setSortingEnabled(prev_sort)
        self.table.resizeColumnsToContents()

    def export_csv(self):
        if not self._last_items:
            QMessageBox.information(self, "Exportar CSV", "No hay datos para exportar.")
            return
        # Suggest a default filename in user's home
        default_path = os.path.expanduser("~/operadores_radio.csv")
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar como…", default_path, "CSV (*.csv)"
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
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
                # Export in alphabetical order by callsign
                for it in sorted(
                    self._last_items, key=lambda x: (str(x.callsign) or "")
                ):
                    writer.writerow(
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
            QMessageBox.information(self, "Exportar CSV", f"Exportado: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Exportar CSV", f"Error al exportar: {e}")

    def closeEvent(self, event):
        try:
            self._save_state()
        finally:
            super().closeEvent(event)

    def _save_state(self):
        settings = QSettings("LoggerOA", "OperatorsDialog")
        header = self.table.horizontalHeader()
        settings.setValue("header_state", header.saveState())
        settings.setValue("sort_column", header.sortIndicatorSection())
        # PySide6 returns a Qt.SortOrder enum; store its numeric value
        try:
            settings.setValue("sort_order", int(header.sortIndicatorOrder().value))
        except Exception:
            # Fallback for environments where .value isn't present
            settings.setValue(
                "sort_order",
                0 if header.sortIndicatorOrder() == Qt.AscendingOrder else 1,
            )
        settings.setValue("filter_text", self.filter_edit.text())
        settings.setValue("field_index", self.field_combo.currentIndex())
        settings.setValue("show_disabled", self.show_disabled_chk.isChecked())

    def _restore_state(self):
        settings = QSettings("LoggerOA", "OperatorsDialog")
        header = self.table.horizontalHeader()
        state = settings.value("header_state")
        if state is not None:
            try:
                header.restoreState(state)
            except Exception:
                pass
        sort_col = settings.value("sort_column")
        sort_ord = settings.value("sort_order")
        try:
            if sort_col is not None:
                col = int(sort_col)
                if sort_ord is not None:
                    try:
                        ord_int = int(sort_ord)
                    except Exception:
                        ord_int = 0
                    order = Qt.SortOrder(ord_int)
                else:
                    order = Qt.AscendingOrder
                self.table.sortItems(col, order)
        except Exception:
            pass
        # Restore filters without spamming signals
        self.filter_edit.blockSignals(True)
        self.field_combo.blockSignals(True)
        self.show_disabled_chk.blockSignals(True)
        ft = settings.value("filter_text")
        if isinstance(ft, str):
            self.filter_edit.setText(ft)
        fi = settings.value("field_index")
        try:
            if fi is not None:
                self.field_combo.setCurrentIndex(int(fi))
        except Exception:
            pass
        sd = settings.value("show_disabled")
        if sd is not None:
            try:
                self.show_disabled_chk.setChecked(bool(int(sd)))
            except Exception:
                try:
                    self.show_disabled_chk.setChecked(bool(sd))
                except Exception:
                    pass
        self.filter_edit.blockSignals(False)
        self.field_combo.blockSignals(False)
        self.show_disabled_chk.blockSignals(False)
