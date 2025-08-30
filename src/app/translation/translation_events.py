from PySide6.QtCore import QObject, Signal


class TranslationSignal(QObject):
    language_changed = Signal()


translation_signal = TranslationSignal()
