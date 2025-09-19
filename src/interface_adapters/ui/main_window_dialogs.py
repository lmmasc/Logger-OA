"""
Módulo de diálogos personalizados para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from PySide6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTextEdit, QPushButton
from utils.resources import get_resource_path
from translation.translation_service import translation_service


def show_about_dialog(self):
    """
    Muestra un cuadro de diálogo con información sobre la aplicación.
    """
    QMessageBox.information(
        self,
        translation_service.tr("about"),
        translation_service.tr("about_message"),
    )


def show_manual_dialog(self):
    """
    Muestra el manual de usuario en un cuadro de diálogo de texto largo.
    """
    # Seleccionar el archivo de manual según el idioma
    lang = translation_service.get_language()
    lang_str = str(lang).lower()
    if "en" in lang_str:
        manual_path = get_resource_path("assets/user_manual_en.md")
        dialog_title = "User Manual"
        close_text = "Close"
    else:
        manual_path = get_resource_path("assets/user_manual_es.md")
        dialog_title = "Manual de uso"
        close_text = "Cerrar"
    manual_text = "Manual not available."
    try:
        with open(manual_path, "r", encoding="utf-8") as f:
            manual_text = f.read()
    except Exception as e:
        manual_text += f"\nError: {e}"
    dialog = QDialog(self)
    dialog.setWindowTitle(dialog_title)
    layout = QVBoxLayout(dialog)
    text_edit = QTextEdit(dialog)
    text_edit.setReadOnly(True)
    text_edit.setPlainText(manual_text)
    layout.addWidget(text_edit)
    close_btn = QPushButton(close_text, dialog)
    close_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_btn)
    dialog.resize(700, 600)

    # Recargar el manual si cambia el idioma mientras el diálogo está abierto
    def reload_manual():
        new_lang = translation_service.get_language()
        new_lang_str = str(new_lang).lower()
        if "en" in new_lang_str:
            new_path = get_resource_path("assets/user_manual_en.md")
            new_title = "User Manual"
            new_close = "Close"
        else:
            new_path = get_resource_path("assets/user_manual_es.md")
            new_title = "Manual de uso"
            new_close = "Cerrar"
        try:
            with open(new_path, "r", encoding="utf-8") as f:
                new_text = f.read()
        except Exception as e:
            new_text = f"Manual not available.\nError: {e}"
        text_edit.setPlainText(new_text)
        dialog.setWindowTitle(new_title)
        close_btn.setText(new_close)

    translation_service.signal.language_changed.connect(reload_manual)
    dialog.exec()
    translation_service.signal.language_changed.disconnect(reload_manual)


# Si hay otros diálogos puros, se pueden agregar aquí como funciones.
