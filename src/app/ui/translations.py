# translations.py

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
    },
}

current_lang = "es"


def tr(key):
    return translations.get(current_lang, translations["es"]).get(key, key)
