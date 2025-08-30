# translations.py

from app.config.settings_manager import SettingsManager

translations = {
    "es": {
        "main_window_title": "Ventana Principal",
        "file_menu": "Archivo",
        "exit": "Salir",
        "help_menu": "Ayuda",
        "about": "Acerca de",
        "aspect_menu": "Aspecto",
        "light_theme": "Tema claro",
        "dark_theme": "Tema oscuro",
        "about_message": "Logger OA v2\nAplicación de ejemplo con PySide6.",
        "language_menu": "Idioma",
        "spanish": "Español",
        "english": "Inglés",
    },
    "en": {
        "main_window_title": "Main Window",
        "file_menu": "File",
        "exit": "Exit",
        "help_menu": "Help",
        "about": "About",
        "aspect_menu": "Appearance",
        "light_theme": "Light Theme",
        "dark_theme": "Dark Theme",
        "about_message": "Logger OA v2\nSample app with PySide6.",
        "language_menu": "Language",
        "spanish": "Spanish",
        "english": "English",
    },
}

settings_mgr = SettingsManager()
current_lang = settings_mgr.get_value("language", "es")


def tr(key):
    return translations.get(current_lang, translations["es"]).get(key, key)


def set_language(lang):
    global current_lang
    if lang in translations:
        current_lang = lang
        settings_mgr.set_value("language", lang)
