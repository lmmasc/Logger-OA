from app.core.translation.translations import TRANSLATIONS


class TranslationService:
    def __init__(self, default_lang="es"):
        self._lang = default_lang

    def set_language(self, lang: str):
        if lang in TRANSLATIONS:
            self._lang = lang

    def get_language(self) -> str:
        return self._lang

    def tr(self, key: str) -> str:
        return TRANSLATIONS.get(self._lang, {}).get(key, key)


# Instancia global para acceso centralizado
translation_service = TranslationService()
