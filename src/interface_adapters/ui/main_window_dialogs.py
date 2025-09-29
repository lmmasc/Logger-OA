"""
Módulo de diálogos personalizados para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from PySide6.QtWidgets import (
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QTextBrowser,
    QPushButton,
)
from utils.resources import get_resource_path
from translation.translation_service import translation_service
import markdown
from version import APP_VERSION, APP_NAME


def show_about_dialog(self):
    """
    Muestra un cuadro de diálogo con información sobre la aplicación.
    """
    base_msg = translation_service.tr("about_message")
    # Agregar versión de la app en el mensaje
    # Evitar 'vv' si APP_VERSION ya incluye prefijo 'v'
    v = str(APP_VERSION).lstrip().lstrip("vV")
    version_line = f"\n\n{APP_NAME} v{v}"
    QMessageBox.information(
        self,
        translation_service.tr("about"),
        base_msg + version_line,
    )


def show_manual_dialog(main_window):
    """
    Muestra el manual de usuario en una ventana no bloqueante.
    Solo permite una instancia abierta a la vez.
    """
    # Si ya está abierta, solo la trae al frente
    if hasattr(main_window, "manual_window") and main_window.manual_window is not None:
        main_window.manual_window.raise_()
        main_window.manual_window.activateWindow()
        return

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
    html_text = "<p>Manual not available.</p>"
    try:
        with open(manual_path, "r", encoding="utf-8") as f:
            manual_text = f.read()
            html_text = markdown.markdown(
                manual_text, extensions=["extra", "tables", "toc"]
            )
    except Exception as e:
        html_text += f"<br>Error: {e}"

    class ManualDialog(QDialog):
        def closeEvent(self, event):
            translation_service.signal.language_changed.disconnect(reload_manual)
            main_window.manual_window = None
            super().closeEvent(event)

    manual_dialog = ManualDialog(main_window)
    manual_dialog.setWindowTitle(dialog_title)
    layout = QVBoxLayout(manual_dialog)
    text_browser = QTextBrowser(manual_dialog)
    text_browser.setOpenExternalLinks(True)
    text_browser.setHtml(html_text)
    layout.addWidget(text_browser)
    close_btn = QPushButton(close_text, manual_dialog)
    close_btn.clicked.connect(manual_dialog.close)
    layout.addWidget(close_btn)
    manual_dialog.resize(800, 700)

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
                new_html = markdown.markdown(
                    new_text, extensions=["extra", "tables", "toc"]
                )
        except Exception as e:
            new_html = f"<p>Manual not available.<br>Error: {e}</p>"
        text_browser.setHtml(new_html)
        manual_dialog.setWindowTitle(new_title)
        close_btn.setText(new_close)

    translation_service.signal.language_changed.connect(reload_manual)
    manual_dialog.show()
    main_window.manual_window = manual_dialog


# Si hay otros diálogos puros, se pueden agregar aquí como funciones.
