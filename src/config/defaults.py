"""
defaults.py

Constantes y valores por defecto globales para la aplicación.
"""

from src.config.settings_service import ThemeValue, LanguageValue

DEFAULT_LANGUAGE = LanguageValue.ES.value
DEFAULT_THEME = ThemeValue.LIGHT.value
APP_NAME = "LoggerOA"
ORG_NAME = "LoggerOAApp"
DATA_DIR = "data"
EXPORT_DIR = "exports"
LOG_DIR = "logs"

# Subfolder names for logs (values in Spanish, used as constants in code)
OPERATIONS_DIR = "operativos"
CONTESTS_DIR = "concursos"
