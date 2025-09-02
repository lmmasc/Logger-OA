"""
settings_service.py

Servicio centralizado para la gestión de configuraciones de la aplicación usando QSettings.
"""

from PySide6.QtCore import QSettings


class SettingsService:
    """
    Servicio para gestionar la configuración persistente de la aplicación.
    Utiliza QSettings para guardar y recuperar valores.
    """

    def __init__(self):
        # Cambia estos valores por los de tu organización y app si lo deseas
        self.settings = QSettings("LoggerOA", "LoggerOAApp")

    def set_value(self, key, value):
        """Guarda un valor en la configuración."""
        self.settings.setValue(key, value)

    def get_value(self, key, default=None):
        """Obtiene un valor de la configuración, o el valor por defecto si no existe."""
        return self.settings.value(key, default)

    def remove(self, key):
        """Elimina una clave de la configuración."""
        self.settings.remove(key)


# Instancia global para acceso centralizado
settings_service = SettingsService()
