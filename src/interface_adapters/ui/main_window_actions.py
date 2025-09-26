import sys
import subprocess

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
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
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


# --- Acciones de Log ---


def action_log_new_operativo(self):
    """
    Crea un nuevo log operativo directamente, sin diálogo de selección de tipo.
    """

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
    # self.setWindowTitle(f"{log.operator} - Operativo - {log.start_time}")
    self.show_view(ViewID.LOG_OPS_VIEW)
    self.update_menu_state()


def action_log_new_concurso(self):
    """
    Crea un nuevo log concurso directamente, sin diálogo de selección de tipo.
    """

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
    # cabecera = f"{log.operator} - {contest_name} - {log.start_time}"
    # self.setWindowTitle(cabecera)
    self.show_view(ViewID.LOG_CONTEST_VIEW)
    self.update_menu_state()


def action_log_open_operativo(self):
    """
    Abre un log operativo existente directamente, sin diálogo de selección de tipo.
    """

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
            # Verificar tipo de log
            if getattr(log, "log_type", None) != LogType.OPERATION_LOG:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    translation_service.tr("log_type_mismatch_error"),
                )
                self.current_log = None
                self.current_log_type = None
                self.show_view(ViewID.WELCOME_VIEW)
                self.update_menu_state()
                return
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
        # Restaurar título original
        self.setWindowTitle(translation_service.tr("main_window_title"))
    self.update_menu_state()


def action_log_open_concurso(self):
    """
    Abre un log concurso existente directamente, sin diálogo de selección de tipo.
    """

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
            # Verificar tipo de log
            if getattr(log, "log_type", None) != LogType.CONTEST_LOG:
                QMessageBox.critical(
                    self,
                    translation_service.tr("main_window_title"),
                    translation_service.tr("log_type_mismatch_error"),
                )
                self.current_log = None
                self.current_log_type = None
                self.show_view(ViewID.WELCOME_VIEW)
                self.update_menu_state()
                return
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
        # Restaurar título original
        self.setWindowTitle(translation_service.tr("main_window_title"))
    self.update_menu_state()


def open_folder_and_select_file(file_path):
    """
    Abre el explorador de archivos en la carpeta del archivo y lo selecciona si es posible.
    Funciona en Windows, macOS y Linux (con fallback).
    """
    folder = os.path.dirname(file_path)
    try:
        if sys.platform.startswith("win"):
            # Windows: explorer /select,"file"
            subprocess.run(["explorer", "/select,", os.path.normpath(file_path)])
        elif sys.platform == "darwin":
            # macOS: open -R "file"
            subprocess.run(["open", "-R", file_path])
        elif sys.platform.startswith("linux"):
            # Linux: intentar con nautilus, dolphin, thunar, luego fallback a xdg-open
            # Selección si posible
            for cmd in [
                ["nautilus", "--select", file_path],
                ["dolphin", "--select", file_path],
                ["thunar", folder],
            ]:
                try:
                    subprocess.Popen(cmd)
                    return
                except FileNotFoundError:
                    continue
            # Fallback: abrir solo la carpeta
            subprocess.Popen(["xdg-open", folder])
        else:
            # Otros sistemas: solo abrir la carpeta
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
    except Exception:
        # Fallback final: abrir la carpeta
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))


def action_log_export_txt(self):
    """
    Exporta el log abierto en formato TXT.
    """
    if not hasattr(self, "current_log") or self.current_log is None:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return
    db_path = getattr(self.current_log, "db_path", None)
    if not db_path:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_db_path"),
        )
        return
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    default_filename = f"{base_name}.txt"
    export_dir = get_export_dir()
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        os.path.join(export_dir, default_filename),
        "TXT (*.txt)",
    )
    if not export_path:
        return
    try:
        export_log.export_log_to_txt(db_path, export_path)
        open_folder_and_select_file(export_path)
    except Exception as e:
        QMessageBox.critical(
            self,
            translation_service.tr("export_log"),
            f"{translation_service.tr('export_failed')}: {e}",
        )


def action_log_export_csv(self):
    """
    Exporta el log abierto en formato CSV.
    """
    if not hasattr(self, "current_log") or self.current_log is None:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return
    db_path = getattr(self.current_log, "db_path", None)
    if not db_path:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_db_path"),
        )
        return
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    default_filename = f"{base_name}.csv"
    export_dir = get_export_dir()
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        os.path.join(export_dir, default_filename),
        "CSV (*.csv)",
    )
    if not export_path:
        return
    try:
        export_log.export_log_to_csv(db_path, export_path)
        open_folder_and_select_file(export_path)
    except Exception as e:
        QMessageBox.critical(
            self,
            translation_service.tr("export_log"),
            f"{translation_service.tr('export_failed')}: {e}",
        )


def action_log_export_adi(self):
    """
    Exporta el log abierto en formato ADI (ADIF).
    """
    if not hasattr(self, "current_log") or self.current_log is None:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return
    db_path = getattr(self.current_log, "db_path", None)
    if not db_path:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_db_path"),
        )
        return
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    default_filename = f"{base_name}.adi"
    export_dir = get_export_dir()
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        os.path.join(export_dir, default_filename),
        "ADI (*.adi)",
    )
    if not export_path:
        return
    try:
        export_log.export_log_to_adi(db_path, export_path)
        open_folder_and_select_file(export_path)
    except Exception as e:
        QMessageBox.critical(
            self,
            translation_service.tr("export_log"),
            f"{translation_service.tr('export_failed')}: {e}",
        )


def action_log_export_pdf(self):
    """
    Exporta el log abierto en formato PDF.
    """
    if not hasattr(self, "current_log") or self.current_log is None:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return
    db_path = getattr(self.current_log, "db_path", None)
    if not db_path:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_db_path"),
        )
        return
    # Verificar tipo de log antes de abrir el selector de archivos
    log_type = getattr(self.current_log, "log_type", None)
    from interface_adapters.ui.view_manager import LogType

    # Permitir tanto Enum como string
    if str(log_type) not in (str(LogType.CONTEST_LOG), LogType.CONTEST_LOG.value):
        QMessageBox.warning(
            self,
            translation_service.tr("export_log"),
            translation_service.tr("export_pdf_not_supported_for_log_type"),
        )
        return
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    default_filename = f"{base_name}.pdf"
    export_dir = get_export_dir()
    export_path, _ = QFileDialog.getSaveFileName(
        self,
        translation_service.tr("export_log"),
        os.path.join(export_dir, default_filename),
        "PDF (*.pdf)",
    )
    if not export_path:
        return
    try:
        export_log.export_log_to_pdf(db_path, export_path)
        open_folder_and_select_file(export_path)
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
    self.setWindowTitle(translation_service.tr("main_window_title"))
    self.update_menu_state()


def action_log_export_simple_text(self):
    """
    Muestra una ventana con el texto simple de exportación (orden, indicativo, nombre) para copiar fácilmente.
    """
    if not hasattr(self, "current_log") or self.current_log is None:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            translation_service.tr("no_log_open"),
        )
        return
    contacts = getattr(self.current_log, "contacts", None)
    if not contacts:
        QMessageBox.warning(
            self,
            translation_service.tr("main_window_title"),
            "No hay contactos en el log actual.",
        )
        return
    # Generar texto formateado tipo tabla para WhatsApp y depuración
    # Calcular el ancho máximo del indicativo
    indicativos = []
    for contact in contacts:
        if isinstance(contact, dict):
            indicativos.append(contact.get("callsign", "-"))
        else:
            indicativos.append(getattr(contact, "callsign", "-"))
    max_callsign_len = max(len(str(i)) for i in indicativos) if indicativos else 10

    # Encabezado con columnas alineadas
    header_num = "Nº"
    header_callsign = translation_service.tr("log_operative_table_header_callsign")
    header_name = translation_service.tr("log_operative_table_header_name")
    lines = [f"{header_num:>2}  {header_callsign:<{max_callsign_len}}  {header_name}"]

    # Filas alineadas
    for idx, contact in enumerate(contacts, 1):
        if isinstance(contact, dict):
            indicativo = contact.get("callsign", "-")
            nombre = contact.get("name", "-")
        else:
            indicativo = getattr(contact, "callsign", "-")
            nombre = getattr(contact, "name", "-")
        lines.append(f"{idx:2d}  {indicativo:<{max_callsign_len}}  {nombre}")
    text = "\n".join(lines)
    # Crear ventana con QTextEdit para copiar
    dialog = QDialog(self)
    dialog.setWindowTitle(translation_service.tr("export_simple_dialog_title"))
    layout = QVBoxLayout(dialog)
    text_edit = QTextEdit(dialog)
    text_edit.setPlainText(text)
    text_edit.setReadOnly(False)  # Permite copiar y editar
    layout.addWidget(text_edit)
    copy_btn = QPushButton(translation_service.tr("export_simple_copy_button"), dialog)
    layout.addWidget(copy_btn)

    def copy_to_clipboard():
        clipboard = QApplication.clipboard()
        clipboard.setText(text_edit.toPlainText())

    copy_btn.clicked.connect(copy_to_clipboard)
    dialog.resize(400, 300)
    dialog.exec()


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


def action_db_import_excel(self):
    """
    Importa operadores OA desde un archivo Excel, mostrando resumen visual.
    """
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        translation_service.tr("import_from_excel"),
        "",
        "Excel Files (*.xlsx);;All Files (*)",
    )
    if file_path:
        wait_dialog = WaitDialog(self)
        wait_dialog.show()
        QApplication.processEvents()

        def do_import():
            try:
                from application.use_cases.update_operators_from_excel import (
                    update_operators_from_excel,
                )

                result = update_operators_from_excel(file_path)
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
                error_msg = translation_service.tr("import_failed")
                if "error" in result:
                    error_msg += f": {result['error']}"
                QMessageBox.warning(
                    self,
                    translation_service.tr("main_window_title"),
                    error_msg,
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
        open_folder_and_select_file(export_path)
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
            from infrastructure.db.reset import clear_database

            clear_database()
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
