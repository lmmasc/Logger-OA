"""
Servicio centralizado para traducción y manejo de idioma en la aplicación.
"""

from app.config.settings_manager import SettingsManager
from app.translation.translations import TRANSLATIONS

# Estado global de idioma
_settings_mgr = SettingsManager()
_current_lang = _settings_mgr.get_value("language", "es")


def tr(key: str) -> str:
    """Traduce una clave según el idioma actual."""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["es"]).get(key, key)


def set_language(lang: str):
    """Cambia el idioma global de la app y lo guarda en settings."""
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang
        _settings_mgr.set_value("language", lang)


def get_language() -> str:
    """Devuelve el idioma actual."""
    return _current_lang


def retranslate_menu_bar(menu_bar, tr_func=None):
    """
    Actualiza los textos de todos los menús y acciones del menú principal.
    Puede ser extendido para otros menús si es necesario.
    """
    if tr_func is None:
        tr_func = tr
    menu_bar.file_menu.setTitle(tr_func("file_menu"))
    menu_bar.open_folder_action.setText(tr_func("open_folder"))
    menu_bar.exit_action.setText(tr_func("exit"))

    # Operativo
    menu_bar.operativo_menu.setTitle(tr_func("ops_menu"))
    menu_bar.ops_new_action.setText(tr_func("new"))
    menu_bar.ops_open_action.setText(tr_func("open"))
    menu_bar.ops_export_action.setText(tr_func("export"))
    menu_bar.ops_close_action.setText(tr_func("close"))

    # Concurso
    menu_bar.concurso_menu.setTitle(tr_func("contest_menu"))
    menu_bar.contest_new_action.setText(tr_func("new"))
    menu_bar.contest_open_action.setText(tr_func("open"))
    menu_bar.contest_export_action.setText(tr_func("export"))
    menu_bar.contest_close_action.setText(tr_func("close"))

    # Base de datos
    menu_bar.database_menu.setTitle(tr_func("database_menu"))
    menu_bar.db_import_pdf_action.setText(tr_func("import_from_pdf"))
    menu_bar.db_export_action.setText(tr_func("export"))
    menu_bar.db_show_action.setText(tr_func("show_database"))

    # Resto
    menu_bar.aspect_menu.setTitle(tr_func("aspect_menu"))
    menu_bar.light_theme_action.setText(tr_func("light_theme"))
    menu_bar.dark_theme_action.setText(tr_func("dark_theme"))
    menu_bar.language_menu.setTitle(tr_func("language_menu"))
    menu_bar.lang_es_action.setText(tr_func("spanish"))
    menu_bar.lang_en_action.setText(tr_func("english"))
    menu_bar.help_menu.setTitle(tr_func("help_menu"))
    menu_bar.about_action.setText(tr_func("about"))


# translation_service.py
"""
Servicio centralizado para traducción y manejo de idioma en la aplicación.
"""
from app.config.settings_manager import SettingsManager
from app.translation.translations import TRANSLATIONS

_settings_mgr = SettingsManager()
_current_lang = _settings_mgr.get_value("language", "es")


def tr(key: str) -> str:
    """Traduce una clave según el idioma actual."""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["es"]).get(key, key)


def set_language(lang: str):
    """Cambia el idioma global de la app y lo guarda en settings."""
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang
        _settings_mgr.set_value("language", lang)


def get_language() -> str:
    """Devuelve el idioma actual."""
    return _current_lang
