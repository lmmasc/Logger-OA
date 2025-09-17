"""
settings_service.py

Servicio centralizado para la gestión de configuraciones de la aplicación usando QSettings.
"""

from PySide6.QtCore import QSettings
from enum import Enum


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


# Enum para las claves de configuración
class SettingsKey(Enum):
    THEME = "theme"
    LANGUAGE = "language"
    # Agrega aquí otras claves según sea necesario


# Enum para los valores posibles de tema
class ThemeValue(Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"
    # Agrega aquí otros valores de tema si existen


# Enum para los valores posibles de idioma
class LanguageValue(Enum):
    ES = "es"
    EN = "en"
    # Agrega aquí otros valores de idioma si existen


# Instancia global para acceso centralizado
settings_service = SettingsService()

# El resto de la lógica y funcionalidad actual se mantiene intacta.
# Cuando se acceda a una clave o valor, usar SettingsKey.THEME.value o ThemeValue.LIGHT.value según corresponda.
# Ejemplo:
# settings[SettingsKey.THEME.value] = ThemeValue.DARK.value
