"""
Handlers de acciones del menú y lógica asociada para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QApplication,
    QComboBox,
)
from PySide6.QtCore import Qt, QUrl, QTimer
import os
from config.paths import get_database_path, get_log_dir
from config.defaults import OPERATIONS_DIR, CONTESTS_DIR
from translation.translation_service import translation_service
from application.use_cases.update_operators_from_pdf import update_operators_from_pdf


def action_log_new(self):
    # ...migrated code from MainWindow._action_log_new...
    dialog = QDialog(self)
    dialog.setWindowTitle(translation_service.tr("select_log_type"))
    dialog.setMinimumWidth(400)
    layout = QVBoxLayout(dialog)
    label = QLabel(translation_service.tr("select_log_type_label_create"))
    layout.addWidget(label)
    btn_ops = QPushButton(translation_service.tr("log_type_ops"), dialog)
    btn_contest = QPushButton(translation_service.tr("log_type_contest"), dialog)
    btn_ops.setFixedWidth(200)
    btn_contest.setFixedWidth(200)
    layout.addWidget(btn_ops, alignment=Qt.AlignHCenter)
    layout.addWidget(btn_contest, alignment=Qt.AlignHCenter)
    selected = {"type": None}

    def select_ops():
        selected["type"] = "operation_log"
        dialog.accept()

    def select_contest():
        selected["type"] = "contest_log"
        dialog.accept()

    btn_ops.clicked.connect(select_ops)
    btn_contest.clicked.connect(select_contest)
    dialog.exec()
    contest_name = None
    if selected["type"] == "contest_log":
        # Diálogo para seleccionar concurso
        contest_dialog = QDialog(self)
        contest_dialog.setWindowTitle(translation_service.tr("select_contest_title"))
        contest_dialog.setMinimumWidth(400)
        contest_layout = QVBoxLayout(contest_dialog)
        contest_label = QLabel(translation_service.tr("select_contest_label"))
        contest_layout.addWidget(contest_label)
        contest_box = QComboBox(contest_dialog)
        contest_options = [
            translation_service.tr("contest_world_radio_day"),
            translation_service.tr("contest_independence_peru"),
            translation_service.tr("contest_peruvian_ham_day"),
        ]
        contest_box.addItems(contest_options)
        contest_layout.addWidget(contest_box, alignment=Qt.AlignHCenter)
        ok_btn = QPushButton(translation_service.tr("ok_button"), contest_dialog)
        ok_btn.setFixedWidth(200)
        contest_layout.addWidget(ok_btn, alignment=Qt.AlignHCenter)

        def set_contest():
            nonlocal contest_name
            contest_name = contest_box.currentText()
            contest_dialog.accept()

        ok_btn.clicked.connect(set_contest)
        contest_dialog.exec()
        if not contest_name:
            return  # Cancelado
    if selected["type"]:
        indicativo_dialog = QDialog(self)
        indicativo_dialog.setWindowTitle(translation_service.tr("enter_callsign"))
        indicativo_dialog.setMinimumWidth(400)
        indicativo_layout = QVBoxLayout(indicativo_dialog)
        indicativo_label = QLabel(translation_service.tr("enter_callsign_label"))
        indicativo_layout.addWidget(indicativo_label)
        callsign_edit = QLineEdit(indicativo_dialog)
        callsign_edit.setFixedWidth(180)
        indicativo_layout.addWidget(callsign_edit, alignment=Qt.AlignHCenter)
        ok_btn = QPushButton(translation_service.tr("ok_button"), indicativo_dialog)
        ok_btn.setFixedWidth(200)
        indicativo_layout.addWidget(ok_btn, alignment=Qt.AlignHCenter)
        indicativo = {"callsign": None}

        def set_callsign():
            from utils.text import normalize_callsign

            indicativo["callsign"] = normalize_callsign(callsign_edit.text().strip())
            indicativo_dialog.accept()

        def normalize_input():
            from utils.text import normalize_callsign

            text = callsign_edit.text()
            normalized = normalize_callsign(text)
            # Evita bucle infinito: solo actualiza si es diferente
            if text != normalized:
                callsign_edit.blockSignals(True)
                callsign_edit.setText(normalized)
                callsign_edit.blockSignals(False)

        callsign_edit.textChanged.connect(normalize_input)
        ok_btn.clicked.connect(set_callsign)
        indicativo_dialog.exec()
        if indicativo["callsign"]:
            from application.use_cases.create_log import create_log

            extra_kwargs = {}
            if selected["type"] == "contest_log":
                contest_keys = [
                    "contest_world_radio_day",
                    "contest_independence_peru",
                    "contest_peruvian_ham_day",
                ]
                contest_key = contest_keys[contest_box.currentIndex()]
                extra_kwargs["contest_key"] = contest_key
                extra_kwargs["name"] = translation_service.tr(contest_key)
                extra_kwargs["metadata"] = {"contest_name_key": contest_key}
            elif selected["type"] == "operation_log":
                from interface_adapters.ui.dialogs.operativo_config_dialog import (
                    OperativoConfigDialog,
                )

                op_dialog = OperativoConfigDialog(self)
                if not op_dialog.exec():
                    return  # Cancelado
                operativo_config = op_dialog.get_config()
                # Pasar tipo y banda para el nombre de archivo
                extra_kwargs["operation_type"] = operativo_config.get(
                    "operation_type", "type"
                )
                extra_kwargs["frequency_band"] = operativo_config.get(
                    "frequency_band", "band"
                )
                extra_kwargs["repeater_key"] = operativo_config.get(
                    "repeater_key", None
                )
                extra_kwargs["metadata"] = operativo_config
            db_path, log = create_log(
                selected["type"], indicativo["callsign"], **extra_kwargs
            )
            self.current_log = log
            self.current_log_type = (
                "ops" if selected["type"] == "operation_log" else "contest"
            )
            # Mostrar en cabecera: Indicativo - nombre del concurso - fecha
            if selected["type"] == "contest_log":
                cabecera = f"{log.operator} - {contest_name} - {log.start_time}"
                self.setWindowTitle(cabecera)
            else:
                self.setWindowTitle(f"{log.operator} - Operativo - {log.start_time}")
            self.show_view(f"log_{self.current_log_type}")
        else:
            self.current_log = None
            self.current_log_type = None
            self.show_view("welcome")
    else:
        self.current_log = None
        self.current_log_type = None
        self.show_view("welcome")
    self.update_menu_state()


def action_log_open(self):
    # ...migrated code from MainWindow._action_log_open...
    dialog = QDialog(self)
    dialog.setWindowTitle(translation_service.tr("select_log_type"))
    dialog.setMinimumWidth(400)
    layout = QVBoxLayout(dialog)
    label = QLabel(translation_service.tr("select_log_type_label_open"))
    layout.addWidget(label)
    btn_ops = QPushButton(translation_service.tr("log_type_ops"), dialog)
    btn_contest = QPushButton(translation_service.tr("log_type_contest"), dialog)
    btn_ops.setFixedWidth(200)
    btn_contest.setFixedWidth(200)
    layout.addWidget(btn_ops, alignment=Qt.AlignHCenter)
    layout.addWidget(btn_contest, alignment=Qt.AlignHCenter)
    selected = {"type": None}

    def select_ops():
        selected["type"] = "operation_log"
        dialog.accept()

    def select_contest():
        selected["type"] = "contest_log"
        dialog.accept()

    btn_ops.clicked.connect(select_ops)
    btn_contest.clicked.connect(select_contest)
    dialog.exec()
    if selected["type"]:
        log_folder = os.path.join(
            get_log_dir(),
            OPERATIONS_DIR if selected["type"] == "operation_log" else CONTESTS_DIR,
        )
        os.makedirs(log_folder, exist_ok=True)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            translation_service.tr("open_log"),
            log_folder,
            "SQLite Files (*.sqlite);;All Files (*)",
        )
        if file_path:
            try:
                from application.use_cases.open_log import open_log

                log = open_log(file_path)
                self.current_log = log
                if hasattr(
                    log, "__class__"
                ) and log.__class__.__name__.lower().startswith("operation"):
                    self.current_log_type = "ops"
                elif hasattr(
                    log, "__class__"
                ) and log.__class__.__name__.lower().startswith("contest"):
                    self.current_log_type = "contest"
                else:
                    self.current_log_type = None
                if self.current_log_type:
                    self.show_view(f"log_{self.current_log_type}")
                else:
                    self.show_view("welcome")
                    self.current_log = None
            except Exception as e:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    f"{translation_service.tr('open_failed')}: {e}",
                )
                self.current_log = None
                self.current_log_type = None
                self.show_view("welcome")
        else:
            self.current_log = None
            self.current_log_type = None
            self.show_view("welcome")
    else:
        self.current_log = None
        self.current_log_type = None
        self.show_view("welcome")
    self.update_menu_state()


def action_log_export(self):
    if not hasattr(self, "current_log") or self.current_log is None:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return

    from application.use_cases.export_log import export_log_to_csv
    from config.paths import get_export_dir

    log_type = getattr(self, "current_log_type", None)
    if log_type not in ("ops", "contest"):
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_type"),
        )
        return

    default_filename = (
        f"{getattr(self.current_log, 'operator', 'log')}_{log_type}_export.csv"
    )
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        get_export_dir(default_filename),
        "CSV Files (*.csv);;All Files (*)",
    )
    if not export_path:
        return

    try:
        db_path = getattr(self.current_log, "db_path", None)
        if not db_path:
            QMessageBox.warning(
                self,
                translation_service.tr("main_window_title"),
                translation_service.tr("no_db_path"),
            )
            return
        export_log_to_csv(db_path, export_path)
        QMessageBox.information(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("export_success"),
        )
    except Exception as e:
        QMessageBox.critical(
            self,
            translation_service.tr("main_window_title"),
            f"{translation_service.tr('export_failed')}: {e}",
        )


def action_log_close(self):
    self.current_log = None
    self.current_log_type = None
    self.show_view("welcome")
    self.update_menu_state()


def action_db_import_pdf(self):
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        translation_service.tr("import_from_pdf"),
        "",
        "PDF Files (*.pdf)",
    )
    if file_path:
        wait_dialog = QDialog(self)
        wait_dialog.setWindowTitle(translation_service.tr("main_window_title"))
        wait_dialog.setModal(True)
        layout = QVBoxLayout(wait_dialog)
        label = QLabel(translation_service.tr("wait_message"))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        wait_dialog.setFixedSize(300, 100)
        wait_dialog.show()
        QApplication.processEvents()

        def do_import():
            try:
                result = update_operators_from_pdf(file_path)
            except Exception as e:
                wait_dialog.close()
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    f"{translation_service.tr('import_failed')}: {e}",
                )
                return
            wait_dialog.close()
            if isinstance(result, dict) and result.get("ok"):
                summary = result
                summary_lines = [
                    translation_service.tr("import_summary_total").format(
                        summary.get("total", 0)
                    ),
                    translation_service.tr("import_summary_new").format(
                        summary.get("new", 0)
                    ),
                    translation_service.tr("import_summary_updated").format(
                        summary.get("updated", 0)
                    ),
                    translation_service.tr("import_summary_unchanged").format(
                        summary.get("unchanged", 0)
                    ),
                    translation_service.tr("import_summary_disabled").format(
                        summary.get("disabled", 0)
                    ),
                    translation_service.tr("import_summary_reenabled").format(
                        summary.get("reenabled", 0)
                    ),
                ]
                if "protected" in summary:
                    summary_lines.append(
                        translation_service.tr("import_summary_protected").format(
                            summary["protected"]
                        )
                    )
                msg = "<br>".join(summary_lines)
                QMessageBox.information(
                    self,
                    translation_service.tr("main_window_title"),
                    msg,
                )
            elif result:
                QMessageBox.information(
                    self,
                    translation_service.tr("main_window_title"),
                    translation_service.tr("import_success"),
                )
            else:
                QMessageBox.warning(
                    self,
                    translation_service.tr("main_window_title"),
                    translation_service.tr("import_failed"),
                )

        QTimer.singleShot(100, do_import)


def action_db_export(self):
    pass


def action_db_delete(self):
    from infrastructure.db.reset import reset_database

    yes_text = translation_service.tr("yes_button")
    no_text = translation_service.tr("no_button")
    box = QMessageBox(self)
    box.setWindowTitle(translation_service.tr("delete_db_confirm"))
    box.setText(translation_service.tr("delete_db_warning"))
    yes_button = box.addButton(yes_text, QMessageBox.YesRole)
    no_button = box.addButton(no_text, QMessageBox.NoRole)
    box.setDefaultButton(no_button)
    box.exec()
    if box.clickedButton() == yes_button:
        try:
            reset_database()
            QMessageBox.information(
                self,
                translation_service.tr("main_window_title"),
                translation_service.tr("delete_db_success"),
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                translation_service.tr("main_window_title"),
                f"{translation_service.tr('import_failed')}: {e}",
            )
    else:
        QMessageBox.information(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("delete_db_cancel"),
        )


def on_menu_action(self, action: str):
    action_map = {
        "log_new": self.action_log_new,
        "log_open": self.action_log_open,
        "log_export": self.action_log_export,
        "log_close": self.action_log_close,
        "db_import_pdf": self.action_db_import_pdf,
        "db_export": self.action_db_export,
        "db_delete": self.action_db_delete,
    }
    handler = action_map.get(action)
    if handler:
        handler()
    else:
        QMessageBox.warning(self, "Acción no implementada", f"No handler for {action}")
