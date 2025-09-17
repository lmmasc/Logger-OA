"""
Módulo de configuración y actualización de la UI para MainWindow.
Cada función recibe la instancia de MainWindow como primer argumento.
"""

from translation.translation_service import translation_service
from config.settings_service import (
    settings_service,
    SettingsKey,
    ThemeValue,
    LanguageValue,
)

# Métodos de configuración y actualización de UI


def set_language(self, lang: LanguageValue) -> None:
    translation_service.set_language(lang)
    current_lang = LanguageValue(
        settings_service.get_value(SettingsKey.LANGUAGE.value, LanguageValue.ES.value)
    )
    if current_lang != lang:
        settings_service.set_value(SettingsKey.LANGUAGE.value, lang.value)
    refresh_ui(self)


def set_light_theme(self) -> None:
    self.theme_manager.apply_theme(ThemeValue.LIGHT)
    settings_service.set_value(SettingsKey.THEME.value, ThemeValue.LIGHT.value)
    refresh_ui(self)


def set_dark_theme(self) -> None:
    self.theme_manager.apply_theme(ThemeValue.DARK)
    settings_service.set_value(SettingsKey.THEME.value, ThemeValue.DARK.value)
    refresh_ui(self)


def set_auto_theme(self) -> None:
    from .themes.system_theme import detect_system_theme

    detected_theme = detect_system_theme()
    self.theme_manager.apply_theme(detected_theme)
    settings_service.set_value(SettingsKey.THEME.value, ThemeValue.AUTO.value)
    refresh_ui(self)


def _update_theme_menu_checks(self) -> None:
    theme = settings_service.get_value(SettingsKey.THEME.value, ThemeValue.LIGHT.value)
    self.menu_bar.light_theme_action.setChecked(theme == ThemeValue.LIGHT.value)
    self.menu_bar.dark_theme_action.setChecked(theme == ThemeValue.DARK.value)
    self.menu_bar.auto_theme_action.setChecked(theme == ThemeValue.AUTO.value)


def _update_language_menu_checks(self) -> None:
    current_lang = translation_service.get_language()
    self.menu_bar.lang_es_action.setChecked(current_lang == LanguageValue.ES)
    self.menu_bar.lang_en_action.setChecked(current_lang == LanguageValue.EN)


def refresh_ui(self) -> None:
    self.setWindowTitle(translation_service.tr("main_window_title"))
    if hasattr(self.menu_bar, "retranslate_ui"):
        self.menu_bar.retranslate_ui()
    for view in self.view_manager.views.values():
        if hasattr(view, "retranslate_ui"):
            view.retranslate_ui()
    if self.db_table_window is not None and hasattr(
        self.db_table_window, "retranslate_ui"
    ):
        self.db_table_window.retranslate_ui()
    _update_language_menu_checks(self)
    _update_theme_menu_checks(self)


def _retranslate_ui(self) -> None:
    self.setWindowTitle(translation_service.tr("main_window_title"))
    if hasattr(self.menu_bar, "retranslate_ui"):
        self.menu_bar.retranslate_ui()
    for view in self.view_manager.views.values():
        if hasattr(view, "retranslate_ui"):
            view.retranslate_ui()


def _set_initial_theme_and_language(self) -> None:
    theme = settings_service.get_value(SettingsKey.THEME.value, ThemeValue.LIGHT.value)
    if theme == ThemeValue.DARK.value:
        set_dark_theme(self)
    elif theme == ThemeValue.LIGHT.value:
        set_light_theme(self)
    elif theme == ThemeValue.AUTO.value:
        set_auto_theme(self)
    lang = LanguageValue(
        settings_service.get_value(SettingsKey.LANGUAGE.value, LanguageValue.ES.value)
    )
    set_language(self, lang)
