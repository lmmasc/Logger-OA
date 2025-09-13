"""
Módulo de diálogos personalizados para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from PySide6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTextEdit, QPushButton
import os, sys
from translation.translation_service import translation_service


def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso, compatible con PyInstaller y multiplataforma.
    Busca el archivo en 'assets/manual_usuario.md' desde la raíz del proyecto.
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller: el archivo se empaqueta en _MEIPASS/assets
        return os.path.join(sys._MEIPASS, "assets", relative_path)
    # Desarrollo: busca desde la raíz del proyecto
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    return os.path.join(base_dir, "assets", relative_path)


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
    manual_path = resource_path("manual_usuario.md")
    manual_text = "Manual de usuario no disponible."
    try:
        with open(manual_path, "r", encoding="utf-8") as f:
            manual_text = f.read()
    except Exception as e:
        manual_text += f"\nError: {e}"
    dialog = QDialog(self)
    dialog.setWindowTitle("Manual de uso")
    layout = QVBoxLayout(dialog)
    text_edit = QTextEdit(dialog)
    text_edit.setReadOnly(True)
    text_edit.setPlainText(manual_text)
    layout.addWidget(text_edit)
    close_btn = QPushButton("Cerrar", dialog)
    close_btn.clicked.connect(dialog.accept)
    layout.addWidget(close_btn)
    dialog.resize(700, 600)
    dialog.exec()


# Si hay otros diálogos puros, se pueden agregar aquí como funciones.
