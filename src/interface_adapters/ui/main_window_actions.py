"""
main_window_actions.py
Acciones y handlers para MainWindow de Logger OA v2.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

# Imports externos
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QApplication,
)
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices

# Imports estándar
import os
from datetime import datetime

# Imports internos
from config.paths import get_database_path, get_log_dir, BASE_PATH, get_export_dir
from config.defaults import OPERATIONS_DIR, CONTESTS_DIR
from config.settings_service import settings_service, CallsignMode
from translation.translation_service import translation_service
from application.use_cases.update_operators_from_pdf import update_operators_from_pdf
from application.use_cases.create_log import create_log
from application.use_cases.open_log import open_log
from application.use_cases import export_log
from interface_adapters.ui.dialogs.wait_dialog import WaitDialog
from interface_adapters.ui.dialogs.select_contest_dialog import SelectContestDialog
from interface_adapters.ui.dialogs.enter_callsign_dialog import EnterCallsignDialog
from interface_adapters.ui.dialogs.operativo_config_dialog import OperativoConfigDialog
from interface_adapters.controllers.database_controller import DatabaseController
from infrastructure.db.reset import reset_database

from .view_manager import ViewID, LogType
from .main_window_db_window import show_db_window, on_db_table_window_closed
from interface_adapters.ui.dialogs.export_format_dialog import ExportFormatDialog


# --- Acciones de Log ---


def action_log_open(self):
    """
    Abre un log existente, seleccionando tipo y archivo.
    """
    log_folder = os.path.join(
        get_log_dir(),
        (
            OPERATIONS_DIR
            if self.current_log_type == LogType.OPERATION_LOG
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
            log = open_log(file_path)
            self.current_log = log
            if hasattr(log, "__class__") and log.__class__.__name__.lower().startswith(
                "operation"
            ):
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
    self.update_menu_state()


def action_log_export(self):
    """
    Exporta el log abierto en el formato seleccionado por el usuario.
    """
    if not hasattr(self, "current_log") or self.current_log is None:
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
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_db_path"),
        )
        return
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    default_filename = f"{base_name}{selected_ext}"
    export_dir = get_export_dir()
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        os.path.join(export_dir, default_filename),
        f"{selected_ext.upper()} (*{selected_ext})",
    )
    if not export_path:
        return
    # Conectar con la función real de exportación
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
        QMessageBox.information(
            self,
            translation_service.tr("export_log"),
            translation_service.tr("export_success"),
        )
    except Exception as e:
        QMessageBox.critical(
            self,
            translation_service.tr("export_log"),
            f"{translation_service.tr('export_failed')}: {e}",
        )


def action_log_close(self):
    """
    Cierra el log actual y vuelve a la vista de bienvenida.
    """
    self.current_log = None
    self.current_log_type = None
    self.show_view(ViewID.WELCOME_VIEW)
    self.update_menu_state()


# --- Acciones de Base de Datos ---
def action_db_import_pdf(self):
    """
    Importa operadores OA desde un PDF oficial, mostrando resumen visual.
    """
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        translation_service.tr("import_from_pdf"),
        "",
        "PDF Files (*.pdf)",
    )
    if file_path:
        wait_dialog = WaitDialog(self)
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
    """
    Exporta la base de datos de operadores a CSV.
    """
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
    """
    Elimina la base de datos local tras confirmación del usuario.
    """

    yes_text = translation_service.tr("yes_button")
    no_text = translation_service.tr("no_button")
    box = QMessageBox(self)
    box.setWindowTitle(translation_service.tr("delete_db_confirm"))
    box.setText(translation_service.tr("delete_db_warning"))
    yes_button = box.addButton(yes_text, QMessageBox.ButtonRole.YesRole)
    no_button = box.addButton(no_text, QMessageBox.ButtonRole.NoRole)
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
                f"{translation_service.tr('delete_db_failed')}: {e}",
            )
    # Si se cancela, no se muestra ningún mensaje


def action_db_backup(self):
    """
    Crea un respaldo de la base de datos y muestra un mensaje informativo.
    """
    try:
        backup_path = DatabaseController.backup_database()
        QMessageBox.information(self, "Backup", f"Backup creado en: {backup_path}")
    except Exception as e:
        QMessageBox.critical(self, "Error", f"No se pudo crear el backup: {e}")


def action_db_restore(self):
    """
    Restaura la base de datos desde un archivo de respaldo seleccionado por el usuario.
    """
    backup_dir = os.path.join(BASE_PATH, "backups")
    file_dialog = QFileDialog(self)
    file_dialog.setWindowTitle("Seleccionar backup para restaurar")
    file_dialog.setDirectory(backup_dir)
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setNameFilter("Backups (*.db)")
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            backup_file = os.path.basename(selected_files[0])
            try:
                DatabaseController.restore_database(backup_file)
                QMessageBox.information(
                    self, "Restaurar", f"Base restaurada desde: {backup_file}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo restaurar: {e}")


def action_db_import_db(self):
    """
    Importa operadores desde una base de datos externa seleccionada por el usuario.
    """
    file_dialog = QFileDialog(self)
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setNameFilter("Bases de datos (*.db)")
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            external_db_path = selected_files[0]
            try:
                imported = DatabaseController.import_database(external_db_path)
                QMessageBox.information(
                    self, "Importar", f"Operadores importados: {imported}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo importar: {e}")


# --- Acciones de UI y ventanas secundarias ---
def action_open_data_folder(self):
    """
    Abre la carpeta donde se guarda la base de datos usando el explorador del sistema.
    """
    db_path = get_database_path()
    folder = os.path.dirname(db_path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(folder))


def action_show_db_window(self):
    """
    Muestra la ventana de gestión de la base de datos.
    """
    show_db_window(self)


def action_on_db_table_window_closed(self, *args):
    """
    Handler para el cierre de la ventana de tabla de base de datos.
    """
    on_db_table_window_closed(self, *args)


# --- Utilidades y helpers ---
def on_menu_action(self, action: str):
    """
    Ejecuta la acción correspondiente según el string recibido.
    """
    action_map = {
        # "log_new": self.action_log_new,  # Eliminado
        "log_open": self.action_log_open,
        "log_export": self.action_log_export,
        "log_close": self.action_log_close,
        "db_import_pdf": self.action_db_import_pdf,
        "db_export": self.action_db_export,
        "db_delete": self.action_db_delete,
        "db_backup": self.action_db_backup,
        "db_restore": self.action_db_restore,
        "db_import_db": self.action_db_import_db,
        "open_data_folder": self.action_open_data_folder,
        "show_db_window": self.action_show_db_window,
    }
    handler = action_map.get(action)
    if handler:
        handler()
    else:
        QMessageBox.warning(self, "Acción no implementada", f"No handler for {action}")


def action_log_new_operativo(self):
    """
    Crea un nuevo log operativo directamente, sin diálogo de selección de tipo.
    """
    # ...existing code...

    callsign_mode = settings_service.get_callsign_mode()
    if callsign_mode == CallsignMode.SAVED:
        indicativo = str(settings_service.get_callsign())
    else:
        indicativo_dialog = EnterCallsignDialog(self)
        if not indicativo_dialog.exec() or not indicativo_dialog.callsign:
            self.current_log = None
            self.current_log_type = None
            self.show_view(ViewID.WELCOME_VIEW)
            self.update_menu_state()
            return
        indicativo = indicativo_dialog.callsign
    op_dialog = OperativoConfigDialog(self)
    if not op_dialog.exec():
        self.current_log = None
        self.current_log_type = None
        self.show_view(ViewID.WELCOME_VIEW)
        self.update_menu_state()
        return
    operativo_config = op_dialog.get_config()
    extra_kwargs = {
        "operation_type": operativo_config.get("operation_type", "type"),
        "frequency_band": operativo_config.get("frequency_band", "band"),
        "repeater_key": operativo_config.get("repeater_key", None),
        "metadata": operativo_config,
    }
    db_path, log = create_log(LogType.OPERATION_LOG, indicativo, **extra_kwargs)
    self.current_log = log
    self.current_log_type = LogType.OPERATION_LOG
    self.setWindowTitle(f"{log.operator} - Operativo - {log.start_time}")
    self.show_view(ViewID.LOG_OPS_VIEW)
    self.update_menu_state()


def action_log_new_concurso(self):
    """
    Crea un nuevo log concurso directamente, sin diálogo de selección de tipo.
    """
    # ...existing code...

    callsign_mode = settings_service.get_callsign_mode()
    if callsign_mode == CallsignMode.SAVED:
        indicativo = str(settings_service.get_callsign())
    else:
        indicativo_dialog = EnterCallsignDialog(self)
        if not indicativo_dialog.exec() or not indicativo_dialog.callsign:
            self.current_log = None
            self.current_log_type = None
            self.show_view(ViewID.WELCOME_VIEW)
            self.update_menu_state()
            return
        indicativo = indicativo_dialog.callsign
    contest_dialog = SelectContestDialog(self)
    if not contest_dialog.exec():
        self.current_log = None
        self.current_log_type = None
        self.show_view(ViewID.WELCOME_VIEW)
        self.update_menu_state()
        return
    contest_name = contest_dialog.selected_contest
    contest_keys = [
        "contest_world_radio_day",
        "contest_independence_peru",
        "contest_peruvian_ham_day",
    ]
    contest_index = contest_dialog.contest_box.currentIndex()
    contest_key = contest_keys[contest_index]
    extra_kwargs = {
        "contest_key": contest_key,
        "name": translation_service.tr(contest_key),
        "metadata": {"contest_name_key": contest_key},
    }
    db_path, log = create_log(LogType.CONTEST_LOG, indicativo, **extra_kwargs)
    self.current_log = log
    self.current_log_type = LogType.CONTEST_LOG
    cabecera = f"{log.operator} - {contest_name} - {log.start_time}"
    self.setWindowTitle(cabecera)
    self.show_view(ViewID.LOG_CONTEST_VIEW)
    self.update_menu_state()


def action_log_open_operativo(self):
    """
    Abre un log operativo existente directamente, sin diálogo de selección de tipo.
    """
    # ...existing code...

    log_folder = os.path.join(get_log_dir(), OPERATIONS_DIR)
    os.makedirs(log_folder, exist_ok=True)
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        translation_service.tr("open_log"),
        log_folder,
        "SQLite Files (*.sqlite);;All Files (*)",
    )
    if file_path:
        try:
            log = open_log(file_path)
            self.current_log = log
            self.current_log_type = LogType.OPERATION_LOG
            self.show_view(ViewID.LOG_OPS_VIEW)
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
    self.update_menu_state()


def action_log_open_concurso(self):
    """
    Abre un log concurso existente directamente, sin diálogo de selección de tipo.
    """
    # ...existing code...

    log_folder = os.path.join(get_log_dir(), CONTESTS_DIR)
    os.makedirs(log_folder, exist_ok=True)
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        translation_service.tr("open_log"),
        log_folder,
        "SQLite Files (*.sqlite);;All Files (*)",
    )
    if file_path:
        try:
            log = open_log(file_path)
            self.current_log = log
            self.current_log_type = LogType.CONTEST_LOG
            self.show_view(ViewID.LOG_CONTEST_VIEW)
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
    self.update_menu_state()
