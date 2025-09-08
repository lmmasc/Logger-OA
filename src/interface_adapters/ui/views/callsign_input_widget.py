from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QScrollArea,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize
from translation.translation_service import translation_service


class CallsignInputWidget(QWidget):
    """
    Widget independiente para el campo de indicativo (callsign).
    Permite reutilización y fácil integración de validaciones/autocompletado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        # Sección izquierda: label encima del campo
        left_box = QVBoxLayout()
        self.label = QLabel("", self)  # Inicializa vacío para traducir luego
        self.input = QLineEdit(self)
        font = QFont()
        font.setPointSize(32)  # Fuente mucho más grande
        font.setBold(True)
        self.input.setFont(font)
        self.input.setMinimumWidth(200)  # Ajuste leve para evitar recorte
        left_box.addWidget(self.label)
        left_box.addWidget(self.input)
        left_widget = QWidget(self)
        left_widget.setLayout(left_box)
        left_widget.setMinimumWidth(200)
        main_layout.addWidget(left_widget, 2)  # Stretch factor bajo para indicativo
        # Sección derecha: resumen y sugerencias
        self.summary_box = QGroupBox("", self)
        self.summary_label = QLabel("", self.summary_box)
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            "padding: 4px; min-height: 40px;"
        )  # Agrega padding interno y altura mínima al label
        summary_font = QFont()
        summary_font.setPointSize(20)
        self.summary_label.setFont(summary_font)
        self.summary_label.setMinimumHeight(40)  # Altura mínima extra
        self.summary_scroll = QScrollArea(self.summary_box)
        self.summary_scroll.setWidgetResizable(True)
        self.summary_scroll.setWidget(self.summary_label)
        self.summary_scroll.setFixedHeight(90)  # Un poco más alto para evitar recortes
        # Sugerencias
        self.suggestion_list = QListWidget(self.summary_box)
        self.suggestion_list.setFixedHeight(90)
        self.suggestion_list.setViewMode(QListWidget.IconMode)
        self.suggestion_list.setFlow(QListWidget.LeftToRight)
        self.suggestion_list.setWrapping(True)
        self.suggestion_list.setResizeMode(QListWidget.Adjust)
        self.suggestion_list.setSpacing(5)  # Espaciado horizontal entre elementos
        self.suggestion_list.hide()
        self.suggestion_list.itemClicked.connect(self._on_suggestion_clicked)
        summary_layout = QVBoxLayout(self.summary_box)
        summary_layout.setContentsMargins(2, 2, 2, 2)  # Reducir márgenes internos
        self.summary_box.setStyleSheet(
            "QGroupBox { padding: 2px; margin-top: 10px; min-height: 110px; }"
        )  # Aumenta min-height para evitar solapamiento del título
        summary_layout.addWidget(self.summary_scroll)
        summary_layout.addWidget(self.suggestion_list)
        self.summary_box.setLayout(summary_layout)
        main_layout.addWidget(self.summary_box, 5)  # Stretch factor alto para resumen
        self.setLayout(main_layout)
        # Normalizar a mayúsculas en tiempo real
        self.input.textChanged.connect(self._normalize_upper)
        # Traducir label y box al crear el widget
        self.retranslate_ui()

    def _normalize_upper(self, text):
        upper_text = text.upper()
        if text != upper_text:
            cursor_pos = self.input.cursorPosition()
            self.input.blockSignals(True)
            self.input.setText(upper_text)
            self.input.setCursorPosition(cursor_pos)
            self.input.blockSignals(False)

    def get_callsign(self):
        return self.input.text()

    def set_callsign(self, value):
        self.input.setText(value.upper())

    def set_summary(self, text, show_suggestions=False):
        if show_suggestions:
            self.summary_scroll.hide()
            self.suggestion_list.show()
            self.suggestion_list.clear()
            indicativos = [
                "OA4ABC",
                "OA2XYZ",
                "OA7DEF",
                "OA4/ON5BAU",
                "OA1QWE",
                "OA3RTY",
                "OA5UIO",
                "OA6PAS",
                "OA7DFG",
                "OA8HJK",
                "OA9LMN",
                "OA0OPQ",
                "OA2RST",
                "OA3UVW",
                "OA4XYZ",
                "OA5ABC",
                "OA6DEF",
                "OA7GHI",
                "OA8JKL",
                "OA9MNO",
                "OA0PQR",
                "OA1STU",
                "OA2VWX",
                "OA3YZA",
                "OA4BCD",
                "OA5EFG",
                "OA6HIJ",
                "OA7KLM",
                "OA8NOP",
                "OA9QRS",
                "OA0TUV",
                "OA1WXY",
                "OA2ZAB",
                "OA3CDE",
                "OA4FGH",
                "OA5IJK",
                "OA6LMN",
                "OA7OPQ",
                "OA8RST",
                "OA9UVW",
                "OA0XYZ",
                "OA1ABC",
                "OA2DEF",
                "OA3GHI",
                "OA4JKL",
                "OA5MNO",
                "OA6PQR",
                "OA7STU",
                "OA8VWX",
                "OA9YZA",
                "OA4/ON5BAU",
                "OA4/ON5BAU",
                "OA4/ON5BAU",
                "OA4/ON5BAU",
            ]
            for indicativo in indicativos:
                item = QListWidgetItem(indicativo)
                font = QFont()
                font.setPointSize(18)
                font.setBold(True)
                item.setFont(font)
                # No modificar el alto ni el ancho, solo usar setSpacing para horizontal
                self.suggestion_list.addItem(item)
        else:
            self.suggestion_list.hide()
            self.summary_scroll.show()
            self.summary_label.setText(text)

    def _on_suggestion_clicked(self, item):
        self.input.setText(item.text())

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("enter_callsign_label"))
        self.summary_box.setTitle(translation_service.tr("callsign_summary"))
        # Si hay un indicativo y existe en la base, regenerar el resumen traducido
        callsign = self.get_callsign().strip().upper()
        if callsign:
            from infrastructure.repositories.sqlite_radio_operator_repository import (
                SqliteRadioOperatorRepository,
            )

            repo = SqliteRadioOperatorRepository()
            operator = (
                repo.get_operator_by_callsign(callsign)
                if hasattr(repo, "get_operator_by_callsign")
                else None
            )
            if operator:
                # Regenerar el resumen traducido
                self.parent()._update_callsign_summary()
