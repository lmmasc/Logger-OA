from __future__ import annotations

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QMenu,
    QMenuBar,
    QFileDialog,
    QMessageBox,
    QProgressDialog,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from ..app import load_app_config
from ..ui.themes import ThemeManager
from ..application.services.import_service import ImportService
from ..application.services.pdf_import_orchestrator import PdfImportOrchestrator
from ..infrastructure.db.sqlite_repo import SqliteRadioOperatorsRepo, SqliteMetaRepo


def main() -> int:
    app = QApplication(sys.argv)
    cfg = load_app_config()
    tm = ThemeManager()
    qss = tm.get_qss(cfg.theme, cfg.font_size)
    app.setStyleSheet(qss)

    win = QMainWindow()
    win.setWindowTitle("Logger OA (Nueva arquitectura)")
    lbl = QLabel("Bienvenido a Logger OA — Nueva estructura")
    lbl.setAlignment(Qt.AlignCenter)
    win.setCentralWidget(lbl)
    win.resize(800, 500)

    # Menu setup
    menubar = QMenuBar(win)
    file_menu = QMenu("&Archivo", win)
    act_import_pdf = QAction("Importar Radioaficionados (PDF)…", win)
    file_menu.addAction(act_import_pdf)
    menubar.addMenu(file_menu)

    view_menu = QMenu("&Ver", win)
    act_view_ops = QAction("Operadores de Radio…", win)
    view_menu.addAction(act_view_ops)
    act_new_operation = QAction("Nuevo Operativo…", win)
    view_menu.addAction(act_new_operation)
    act_new_contest = QAction("Nuevo Concurso…", win)
    view_menu.addAction(act_new_contest)
    act_open_operation = QAction("Abrir Operativo…", win)
    view_menu.addAction(act_open_operation)
    act_open_contest = QAction("Abrir Concurso…", win)
    view_menu.addAction(act_open_contest)
    menubar.addMenu(view_menu)

    tools_menu = QMenu("&Herramientas", win)
    act_db_info = QAction("Información de la base…", win)
    tools_menu.addAction(act_db_info)
    menubar.addMenu(tools_menu)
    win.setMenuBar(menubar)

    def on_import_pdf():
        pdf_path, _ = QFileDialog.getOpenFileName(
            win, "Seleccionar PDF de Radioaficionados", "", "PDF (*.pdf)"
        )
        if not pdf_path:
            return

        # Single progress dialog for both phases
        progress = QProgressDialog("Preparando importación…", "Cancelar", 0, 0, win)
        progress.setWindowTitle("Importar Radioaficionados")
        progress.setMinimumDuration(0)
        progress.setAutoClose(False)
        progress.setAutoReset(False)
        canceled = {"flag": False}

        def on_canceled():
            canceled["flag"] = True

        try:
            progress.canceled.connect(on_canceled)
        except Exception:
            pass

        total_pages = 0

        def parse_cb(i: int, total: int):
            nonlocal total_pages
            if canceled["flag"]:
                raise RuntimeError("Importación cancelada por el usuario")
            if total_pages != total:
                total_pages = total
                progress.setRange(0, total)
            progress.setLabelText("Analizando PDF…")
            progress.setValue(i)
            QApplication.processEvents()

        try:
            repo = SqliteRadioOperatorsRepo()
            repo.init_schema()
            svc = ImportService(repo)
            meta = SqliteMetaRepo()
            orch = PdfImportOrchestrator(svc, meta_repo=meta)

            def import_cb(done: int, total: int, phase: str):
                if canceled["flag"]:
                    raise RuntimeError("Importación cancelada por el usuario")
                progress.setLabelText("Importando registros…")
                progress.setRange(0, 0)  # busy
                QApplication.processEvents()

            # The orchestrator will parse and import, persist last_pdf_date in meta
            result = orch.import_radio_operators_from_pdf(
                pdf_path,
                cutoff_date="01/01/1900",
                parse_progress=parse_cb,
                import_progress=import_cb,
            )
        except Exception as e:
            progress.close()
            # Distinguish user cancel from real error
            if "cancelada" in str(e).lower():
                QMessageBox.information(
                    win, "Importación cancelada", "La importación fue cancelada."
                )
            else:
                QMessageBox.critical(win, "Error al importar", str(e))
            return
        finally:
            progress.close()

        # Retrieve last PDF cutoff date if available
        last_pdf_date = None
        try:
            meta = SqliteMetaRepo()
            last_pdf_date = meta.get("last_pdf_date")
        except Exception:
            last_pdf_date = None

        # Show counters and cutoff date
        msg = ""
        if last_pdf_date:
            msg += f"Fecha corte PDF: {last_pdf_date}\n"
        msg += (
            f"Altas: {result.created}  Actualizados: {result.updated}  Rehabilitados: {result.reenabled}\n"
            f"Deshabilitados (OA): {result.disabled_oa}\n"
            f"Escrituras totales: {result.total_upserts}"
        )
        QMessageBox.information(win, "Importación completada", msg)

    act_import_pdf.triggered.connect(on_import_pdf)

    def on_view_ops():
        from ..ui.operators_dialog import RadioOperatorsDialog

        dlg = RadioOperatorsDialog(win)
        dlg.exec()

    act_view_ops.triggered.connect(on_view_ops)

    def on_new_operation():
        from ..ui.operation_dialog import OperationDialog

        dlg = OperationDialog(win)
        dlg.exec()

    act_new_operation.triggered.connect(on_new_operation)

    def on_new_contest():
        from ..ui.contest_dialog import ContestDialog

        dlg = ContestDialog(win)
        dlg.exec()

    def on_open_operation():
        from ..ui.operation_dialog import OperationDialog
        from ..infrastructure.files.json_repo import JsonOperationsRepo

        from PySide6.QtCore import QSettings

        settings = QSettings("LoggerOA", "DesktopRunner")
        last_dir = settings.value("last_open_operation") or ""
        path, _ = QFileDialog.getOpenFileName(
            win, "Abrir operativo…", last_dir, "Operativo (*.json)"
        )
        if not path:
            return
        try:
            repo = JsonOperationsRepo()
            op = repo.load(path)
        except Exception as e:
            QMessageBox.critical(win, "Abrir operativo", f"Error: {e}")
            return
        settings.setValue("last_open_operation", path)
        dlg = OperationDialog(win, op=op)
        dlg.exec()

    act_open_operation.triggered.connect(on_open_operation)

    def on_open_contest():
        from ..ui.contest_dialog import ContestDialog
        from ..infrastructure.files.json_repo import JsonContestsRepo

        from PySide6.QtCore import QSettings

        settings = QSettings("LoggerOA", "DesktopRunner")
        last_dir = settings.value("last_open_contest") or ""
        path, _ = QFileDialog.getOpenFileName(
            win, "Abrir concurso…", last_dir, "Concurso (*.json)"
        )
        if not path:
            return
        try:
            repo = JsonContestsRepo()
            c = repo.load(path)
        except Exception as e:
            QMessageBox.critical(win, "Abrir concurso", f"Error: {e}")
            return
        settings.setValue("last_open_contest", path)
        dlg = ContestDialog(win, contest=c)
        dlg.exec()

    act_open_contest.triggered.connect(on_open_contest)

    act_new_contest.triggered.connect(on_new_contest)

    def on_db_info():
        from ..ui.db_info_dialog import DatabaseInfoDialog

        dlg = DatabaseInfoDialog(win)
        dlg.exec()

    act_db_info.triggered.connect(on_db_info)

    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
