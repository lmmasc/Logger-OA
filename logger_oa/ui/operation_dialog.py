from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import QSettings
from PySide6.QtGui import QKeySequence, QShortcut

from ..application.services.operations_service import OperationsService
from ..infrastructure.files.json_repo import JsonOperationsRepo
from ..domain.models import Operation, OperationContact


class OperationDialog(QDialog):
    def __init__(self, parent=None, op: Operation | None = None):
        super().__init__(parent)
        self.setWindowTitle("Operativo[*]")
        self.resize(900, 600)
        # state
        self._dirty = False
        self._loading = True
        self.setWindowModified(False)

        self.repo = JsonOperationsRepo()
        self.svc = OperationsService(self.repo)
        self.op = (
            op
            if op is not None
            else self.svc.new_operation(type="GENERIC", operator="")
        )

        # Header form
        self.ed_name = QLineEdit(self)
        self.ed_operator = QLineEdit(self)
        self.cb_band = QComboBox(self)
        self.cb_band.addItems(["", "HF", "VHF", "UHF"])
        self.cb_mode = QComboBox(self)
        self.cb_mode.addItems(["", "SSB", "FM", "CW", "FT8"])

        header = QHBoxLayout()
        header.addWidget(QLabel("Nombre:"))
        header.addWidget(self.ed_name, 2)
        header.addWidget(QLabel("Operador:"))
        header.addWidget(self.ed_operator, 1)
        header.addWidget(QLabel("Banda:"))
        header.addWidget(self.cb_band, 1)
        header.addWidget(QLabel("Modo:"))
        header.addWidget(self.cb_mode, 1)

        # Contacts table (minimal)
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Callsign", "Nombre", "RS RX", "RS TX", "Obs"]
        )

        # Buttons
        btns = QHBoxLayout()
        self.btn_add = QPushButton("Añadir contacto", self)
        self.btn_save = QPushButton("Guardar…", self)
        btns.addWidget(self.btn_add)
        btns.addStretch(1)
        btns.addWidget(self.btn_save)

        lay = QVBoxLayout(self)
        lay.addLayout(header)
        lay.addWidget(self.table, 1)
        lay.addLayout(btns)

        # wiring
        self.btn_add.clicked.connect(self._on_add_contact)
        self.btn_save.clicked.connect(self._on_save)
        # shortcuts
        QShortcut(QKeySequence.Save, self, self._on_save)

        # tab order / focus
        try:
            self.setTabOrder(self.ed_name, self.ed_operator)
            self.setTabOrder(self.ed_operator, self.cb_band)
            self.setTabOrder(self.cb_band, self.cb_mode)
            self.setTabOrder(self.cb_mode, self.table)
        except Exception:
            pass

        # If loaded op provided, reflect header fields
        if self.op:
            band_ix = self.cb_band.findText(self.op.band)
            if band_ix >= 0:
                self.cb_band.setCurrentIndex(band_ix)
            mode_ix = self.cb_mode.findText(self.op.mode)
            if mode_ix >= 0:
                self.cb_mode.setCurrentIndex(mode_ix)
            self.ed_operator.setText(self.op.operator or "")

        self._restore_state()
        self._refresh()
        self._loading = False
        self._wire_dirty_signals()

    def _refresh(self):
        # avoid emitting itemChanged while populating
        self._loading = True
        try:
            self.table.blockSignals(True)
            self.table.setRowCount(len(self.op.stations))
            for row, s in enumerate(self.op.stations):
                self.table.setItem(row, 0, QTableWidgetItem(s.callsign))
                self.table.setItem(row, 1, QTableWidgetItem(s.name))
                self.table.setItem(row, 2, QTableWidgetItem(s.rs_rx))
                self.table.setItem(row, 3, QTableWidgetItem(s.rs_tx))
                self.table.setItem(row, 4, QTableWidgetItem(s.obs))
        finally:
            self.table.blockSignals(False)
            self._loading = False

    def _on_add_contact(self):
        s = OperationContact(callsign="", name="-", rs_rx="59", rs_tx="59", obs="-")
        self.svc.add_contact(self.op, s)
        self._refresh()
        self._mark_dirty()
        # focus first cell of the new row for quick entry
        try:
            row = max(0, self.table.rowCount() - 1)
            self.table.setCurrentCell(row, 0)
            self.table.editItem(self.table.item(row, 0))
        except Exception:
            pass

    def _on_save(self) -> bool:
        # update op header from form
        self.op.operator = self.ed_operator.text()
        self.op.type = "GENERIC"
        self.op.band = self.cb_band.currentText()
        self.op.mode = self.cb_mode.currentText()

        # simple validations
        if not (self.op.operator or "").strip():
            QMessageBox.warning(self, "Operativo", "Completa el campo Operador.")
            return False

        # choose path
        settings = QSettings("LoggerOA", "OperationDialog")
        last_dir = settings.value("last_dir") or ""
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar operativo…", last_dir, "Operativo (*.json)"
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
            self.svc.save(self.op, path)
            QMessageBox.information(self, "Operativo", f"Guardado en: {path}")
            self._dirty = False
            self.setWindowModified(False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Operativo", f"Error al guardar: {e}")
            return False

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
            # Discard falls through to close
        try:
            self._save_state()
        finally:
            super().closeEvent(event)

    def _save_state(self):
        settings = QSettings("LoggerOA", "OperationDialog")
        settings.setValue("name", self.ed_name.text())
        settings.setValue("operator", self.ed_operator.text())
        settings.setValue("band", self.cb_band.currentText())
        settings.setValue("mode", self.cb_mode.currentText())

    def _restore_state(self):
        settings = QSettings("LoggerOA", "OperationDialog")
        self.ed_name.setText(settings.value("name") or "")
        self.ed_operator.setText(settings.value("operator") or "")
        band = settings.value("band") or ""
        mode = settings.value("mode") or ""
        ix_b = self.cb_band.findText(band)
        if ix_b >= 0:
            self.cb_band.setCurrentIndex(ix_b)
        ix_m = self.cb_mode.findText(mode)
        if ix_m >= 0:
            self.cb_mode.setCurrentIndex(ix_m)

    def _wire_dirty_signals(self):
        # mark dirty when header fields or table change
        self.ed_name.textChanged.connect(self._mark_dirty)
        self.ed_operator.textChanged.connect(self._mark_dirty)
        self.cb_band.currentIndexChanged.connect(self._mark_dirty)
        self.cb_mode.currentIndexChanged.connect(self._mark_dirty)
        self.table.itemChanged.connect(self._on_table_item_changed)

    def _on_table_item_changed(self, *args):
        self._mark_dirty()

    def _mark_dirty(self, *args):
        if self._loading:
            return
        self._dirty = True
        self.setWindowModified(True)
