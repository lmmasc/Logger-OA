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
from interface_adapters.ui.dialogs.select_log_type_dialog import SelectLogTypeDialog
from interface_adapters.ui.dialogs.select_contest_dialog import SelectContestDialog
from interface_adapters.ui.dialogs.enter_callsign_dialog import EnterCallsignDialog
from .view_manager import ViewID, LogType


def action_log_new(self):
    # Diálogo modularizado para seleccionar tipo de log
    dialog = SelectLogTypeDialog(self)
    if not dialog.exec():
        self.current_log = None
        self.current_log_type = None
        self.show_view(ViewID.WELCOME_VIEW)
        self.update_menu_state()
        return
    selected = {"type": dialog.selected_type}  # dialog.selected_type ya es LogType Enum
    contest_name = None
    if selected["type"]:
        indicativo_dialog = EnterCallsignDialog(self)
        if not indicativo_dialog.exec() or not indicativo_dialog.callsign:
            self.current_log = None
            self.current_log_type = None
            self.show_view(ViewID.WELCOME_VIEW)
            self.update_menu_state()
            return
        indicativo = {"callsign": indicativo_dialog.callsign}

        if selected["type"] == LogType.CONTEST_LOG:
            contest_dialog = SelectContestDialog(self)
            if not contest_dialog.exec():
                self.current_log = None
                self.current_log_type = None
                self.show_view(ViewID.WELCOME_VIEW)
                self.update_menu_state()
                return
            contest_name = contest_dialog.selected_contest

        if indicativo["callsign"]:
            from application.use_cases.create_log import create_log

            extra_kwargs = {}
            if selected["type"] == LogType.CONTEST_LOG:
                contest_keys = [
                    "contest_world_radio_day",
                    "contest_independence_peru",
                    "contest_peruvian_ham_day",
                ]
                contest_index = contest_dialog.contest_box.currentIndex()
                contest_key = contest_keys[contest_index]
                extra_kwargs["contest_key"] = contest_key
                extra_kwargs["name"] = translation_service.tr(contest_key)
                extra_kwargs["metadata"] = {"contest_name_key": contest_key}
            elif selected["type"] == LogType.OPERATION_LOG:
                from interface_adapters.ui.dialogs.operativo_config_dialog import (
                    OperativoConfigDialog,
                )

                op_dialog = OperativoConfigDialog(self)
                if not op_dialog.exec():
                    return  # Cancelado
                operativo_config = op_dialog.get_config()
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
            self.current_log_type = selected["type"]
            if self.current_log_type == LogType.CONTEST_LOG:
                cabecera = f"{log.operator} - {contest_name} - {log.start_time}"
                self.setWindowTitle(cabecera)
            else:
                self.setWindowTitle(f"{log.operator} - Operativo - {log.start_time}")
            if self.current_log_type == LogType.OPERATION_LOG:
                self.show_view(ViewID.LOG_OPS_VIEW)
            elif self.current_log_type == LogType.CONTEST_LOG:
                self.show_view(ViewID.LOG_CONTEST_VIEW)
            else:
                self.show_view(ViewID.WELCOME_VIEW)
        else:
            self.current_log = None
            self.current_log_type = None
            self.show_view(ViewID.WELCOME_VIEW)
    else:
        self.current_log = None
        self.current_log_type = None
        self.show_view(ViewID.WELCOME_VIEW)
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
        selected["type"] = LogType.OPERATION_LOG
        dialog.accept()

    def select_contest():
        selected["type"] = LogType.CONTEST_LOG
        dialog.accept()

    btn_ops.clicked.connect(select_ops)
    btn_contest.clicked.connect(select_contest)
    dialog.exec()
    if selected["type"]:
        log_folder = os.path.join(
            get_log_dir(),
            (
                OPERATIONS_DIR
                if selected["type"] == LogType.OPERATION_LOG
                else CONTESTS_DIR
            ),
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
                    self.current_log_type = LogType.OPERATION_LOG
                elif hasattr(
                    log, "__class__"
                ) and log.__class__.__name__.lower().startswith("contest"):
                    self.current_log_type = LogType.CONTEST_LOG
                else:
                    self.current_log_type = None
                if self.current_log_type == LogType.OPERATION_LOG:
                    self.show_view(ViewID.LOG_OPS_VIEW)
                elif self.current_log_type == LogType.CONTEST_LOG:
                    self.show_view(ViewID.LOG_CONTEST_VIEW)
                else:
                    self.show_view(ViewID.WELCOME_VIEW)
                    self.current_log = None
            except Exception as e:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    f"{translation_service.tr('open_failed')}: {e}",
                )
                self.current_log = None
                self.current_log_type = None
                self.show_view(ViewID.WELCOME_VIEW)
        else:
            self.current_log = None
            self.current_log_type = None
            self.show_view(ViewID.WELCOME_VIEW)
    else:
        self.current_log = None
        self.current_log_type = None
        self.show_view(ViewID.WELCOME_VIEW)
    self.update_menu_state()


def action_log_export(self):
    if not hasattr(self, "current_log") or self.current_log is None:
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return
    log_type = getattr(self, "current_log_type", None)
    dialog = ExportFormatDialog(log_type, self)
    if not dialog.exec() or not dialog.selected_ext:
        return
    selected_ext = dialog.selected_ext
    db_path = getattr(self.current_log, "db_path", None)
    if not db_path:
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_db_path"),
        )
        return
    import os

    base_name = os.path.splitext(os.path.basename(db_path))[0]
    default_filename = f"{base_name}{selected_ext}"
    from config.paths import get_export_dir

    export_dir = get_export_dir()
    from PySide6.QtWidgets import QFileDialog

    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        os.path.join(export_dir, default_filename),
        f"{selected_ext.upper()} (*{selected_ext})",
    )
    if not export_path:
        return
    # Conectar con la función real de exportación
    from application.use_cases import export_log

    try:
        if selected_ext == ".txt":
            export_log.export_log_to_txt(db_path, export_path)
        elif selected_ext == ".csv":
            export_log.export_log_to_csv(db_path, export_path)
        elif selected_ext == ".adi":
            export_log.export_log_to_adi(db_path, export_path)
        elif selected_ext == ".pdf":
            export_log.export_log_to_pdf(db_path, export_path)
        else:
            raise ValueError(f"Formato no soportado: {selected_ext}")
        # ...existing code...
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.information(
            self,
            translation_service.tr("export_log"),
            translation_service.tr("export_success"),
        )
    except Exception as e:
        # ...existing code...
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.critical(
            self,
            translation_service.tr("export_log"),
            f"{translation_service.tr('export_failed')}: {e}",
        )


def action_log_close(self):
    self.current_log = None
    self.current_log_type = None
    self.show_view(ViewID.WELCOME_VIEW)
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
    from interface_adapters.controllers.database_controller import DatabaseController
    from translation.translation_service import translation_service
    from PySide6.QtWidgets import QFileDialog, QMessageBox
    import os

    from config.paths import get_export_dir

    from datetime import datetime

    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_filename = f"operadores_export_{now_str}.csv"
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_db"),
        get_export_dir(default_filename),
        "CSV Files (*.csv);;All Files (*)",
    )
    if not export_path:
        return
    try:
        DatabaseController.export_database_to_csv(export_path, translation_service)
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


from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton


class ExportFormatDialog(QDialog):
    def __init__(self, log_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translation_service.tr("export_log"))
        layout = QVBoxLayout(self)
        label = QLabel(translation_service.tr("select_export_format"))
        layout.addWidget(label)
        self.combo = QComboBox(self)
        # Usar Enum LogType para decidir los formatos
        if log_type == LogType.OPERATION_LOG:
            self.formats = [
                ("TXT", ".txt"),
                ("CSV", ".csv"),
                ("ADI", ".adi"),
            ]
        elif log_type == LogType.CONTEST_LOG:
            self.formats = [
                ("PDF", ".pdf"),
                ("CSV", ".csv"),
                ("ADI", ".adi"),
            ]
        else:
            raise ValueError(f"Tipo de log no soportado: {log_type}")
        self.combo.addItems([f[0] for f in self.formats])
        layout.addWidget(self.combo)
        btn_ok = QPushButton(translation_service.tr("ok_button"), self)
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)
        self.selected_ext = None

    def accept(self):
        idx = self.combo.currentIndex()
        self.selected_ext = self.formats[idx][1]
        super().accept()
