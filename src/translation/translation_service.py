from PySide6.QtCore import QObject, Signal
from .translations import load_translations
from config.settings_service import LanguageValue


class TranslationSignal(QObject):
    language_changed = Signal()


class TranslationService:
    def __init__(self, default_lang=LanguageValue.ES):
        """
        Inicializa el servicio de traducción con un idioma por defecto.
        :param default_lang: Enum LanguageValue inicial (por defecto LanguageValue.ES).
        """
        self._lang = default_lang
        self._signal = TranslationSignal()
        self._translations = load_translations(self._lang)

    def set_language(self, lang: LanguageValue):
        """
        Cambia el idioma actual del servicio y emite la señal de cambio de idioma si el idioma es válido.
        :param lang: Enum LanguageValue a establecer.
        """
        translations = load_translations(lang)
        if translations:
            self._lang = lang
            self._translations = translations
            self._signal.language_changed.emit()

    @property
    def signal(self):
        """Permite acceder a la señal de cambio de idioma desde el servicio."""
        return self._signal

    def get_language(self) -> LanguageValue:
        """
        Devuelve el enum LanguageValue actualmente seleccionado.
        :return: Enum LanguageValue actual.
        """
        return self._lang

    def tr(self, key: str) -> str:
        """
        Traduce una clave dada al idioma actual. Si la clave no existe, retorna la clave original.
        :param key: Clave de traducción.
        :return: Traducción correspondiente o la clave si no existe.
        """
        return self._translations.get(key, key)


# Instancia global para acceso centralizado
default_lang = LanguageValue.ES
translation_service = TranslationService(default_lang)
