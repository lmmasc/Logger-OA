# Loader central de traducciones modularizadas
import importlib
from utils.resources import get_resource_path
from config.settings_service import LanguageValue

TRANSLATION_MODULES = [
    "ui",
    "menu",
    "log_ops",
    "log_contest",
    "table_headers",
    "messages",
    "forms",
    "operator",
    "import_summary",
    # Agrega aquí más módulos según crezcan las secciones
]


def load_translations(lang_code: LanguageValue):
    """
    Carga y combina los diccionarios de traducción para el idioma dado desde src/translation/<lang_code>/.
    lang_code debe ser LanguageValue
    """
    translations = {}
    lang_str = (
        lang_code.value if isinstance(lang_code, LanguageValue) else str(lang_code)
    )
    for module_name in TRANSLATION_MODULES:
        try:
            mod = importlib.import_module(f"translation.{lang_str}.{module_name}")
            dict_name = f"{module_name.upper()}_TRANSLATIONS"
            section = getattr(mod, dict_name, {})
            translations.update(section)
        except Exception:
            pass  # Si el módulo no existe, lo ignora
    # Ejemplo de uso universal si se cargan archivos:
    # path = get_resource_path(f"src/translation/{lang_str}/{module_name}.py")
    return translations


# Ejemplo de uso:
# translations = load_translations(LanguageValue.ES)
