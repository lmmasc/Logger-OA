from PySide6.QtCore import QObject, Signal
from .translations import TRANSLATIONS


class TranslationSignal(QObject):
    language_changed = Signal()


class TranslationService:
    def __init__(self, default_lang="es"):
        """
        Inicializa el servicio de traducción con un idioma por defecto.
        :param default_lang: Código de idioma inicial (por defecto 'es').
        """
        self._lang = default_lang
        self._signal = TranslationSignal()

    def set_language(self, lang: str):
        """
        Cambia el idioma actual del servicio y emite la señal de cambio de idioma si el idioma es válido.
        :param lang: Código de idioma a establecer.
        """
        if lang in TRANSLATIONS:
            self._lang = lang
            self._signal.language_changed.emit()

    @property
    def signal(self):
        """Permite acceder a la señal de cambio de idioma desde el servicio."""
        return self._signal

    def get_language(self) -> str:
        """
        Devuelve el código del idioma actualmente seleccionado.
        :return: Código de idioma actual.
        """
        return self._lang

    def tr(self, key: str) -> str:
        """
        Traduce una clave dada al idioma actual. Si la clave no existe, retorna la clave original.
        :param key: Clave de traducción.
        :return: Traducción correspondiente o la clave si no existe.
        """
        return TRANSLATIONS.get(self._lang, {}).get(key, key)


# Instancia global para acceso centralizado
translation_service = TranslationService()
