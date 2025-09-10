"""
CallsignInfoWidget: Widget para mostrar información y sugerencias de indicativos.
- Presenta título dinámico, resumen y lista de sugerencias.
- Permite selección de sugerencia y adaptación a idioma.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, Qt
from translation.translation_service import translation_service
from utils.text import get_filtered_operators


class CallsignInfoWidget(QWidget):
    """
    Widget para mostrar información y sugerencias de indicativos.
    Presenta un título dinámico, un área de resumen y una lista de sugerencias.
    """

    suggestionSelected = Signal(str)

    def __init__(self, parent=None):
        """
        Inicializa el widget de información de indicativo.
        Args:
            parent (QWidget): Widget padre.
        """
        super().__init__(parent)
        self._showing_suggestions = False
        self._current_callsign = ""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        # Título dinámico
        self.title_label = QLabel("", self)
        title_font = QFont()
        title_font.setPointSize(14)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)
        # Resumen
        self.summary_label = QLabel("", self)
        self.summary_label.setObjectName("summary-label")
        self.summary_label.setWordWrap(True)
        summary_font = QFont()
        summary_font.setPointSize(20)
        self.summary_label.setFont(summary_font)
        self.summary_label.setMinimumHeight(90)
        self.summary_label.setMaximumHeight(90)
        layout.addWidget(self.summary_label)
        # Sugerencias
        self.suggestion_list = QListWidget(self)
        self.suggestion_list.setMinimumHeight(90)
        self.suggestion_list.setMaximumHeight(90)
        self.suggestion_list.setViewMode(QListWidget.IconMode)
        self.suggestion_list.setFlow(QListWidget.LeftToRight)
        self.suggestion_list.setWrapping(True)
        self.suggestion_list.setResizeMode(QListWidget.Adjust)
        self.suggestion_list.setSpacing(5)
        self.suggestion_list.setObjectName("CallsignSuggestionList")
        self.suggestion_list.hide()
        self.suggestion_list.itemClicked.connect(self._on_suggestion_clicked)
        layout.addWidget(self.suggestion_list)
        self.setLayout(layout)
        self.retranslate_ui()
        translation_service.signal.language_changed.connect(self.retranslate_ui)

    def show_summary(self, text):
        """
        Muestra el resumen del indicativo en el área correspondiente.
        Args:
            text (str): HTML o texto plano con el resumen.
        """
        self._showing_suggestions = False
        self.suggestion_list.hide()
        self.summary_label.show()
        self.summary_label.setText(text)
        self.title_label.setText(translation_service.tr("callsign_summary"))

    def show_suggestions(self, filtro):
        """
        Muestra la lista de sugerencias filtradas por el texto ingresado.
        Args:
            filtro (str): Texto para filtrar operadores.
        """
        self._showing_suggestions = True
        self.summary_label.hide()
        self.suggestion_list.show()
        self.suggestion_list.clear()
        operadores = (
            get_filtered_operators(filtro) if filtro and len(filtro) >= 2 else []
        )
        for op in operadores:
            item = QListWidgetItem(op.callsign)
            font = QFont()
            font.setPointSize(18)
            font.setBold(True)
            item.setFont(font)
            if op.name:
                item.setToolTip(op.name)
            self.suggestion_list.addItem(item)
        self.title_label.setText(translation_service.tr("suggestions_label"))

    def _on_suggestion_clicked(self, item):
        """
        Emite la señal cuando se selecciona una sugerencia.
        Args:
            item (QListWidgetItem): Item seleccionado.
        """
        self.suggestionSelected.emit(item.text())

    def retranslate_ui(self):
        """
        Actualiza el título según el estado actual (sugerencias o resumen).
        """
        if self._showing_suggestions:
            self.title_label.setText(translation_service.tr("suggestions_label"))
        else:
            self.title_label.setText(translation_service.tr("callsign_summary"))

    def update_info(self, text):
        """
        Actualiza el área de información según el texto ingresado.
        Muestra sugerencias si hay más de 2 caracteres, o el resumen si hay coincidencia exacta.
        Args:
            text (str): Texto ingresado para buscar operadores.
        """
        filtro = text.strip().upper()
        if len(filtro) < 2:
            self.show_suggestions("")
        else:
            operadores = get_filtered_operators(filtro)
            exact_matches = [op for op in operadores if op.callsign.upper() == filtro]
            if len(exact_matches) == 1:
                operator = exact_matches[0]
                enabled = (
                    translation_service.tr("enabled")
                    if operator.enabled
                    else translation_service.tr("disabled")
                )
                summary = f"<table width='100%' style='font-size:16px;'>"
                summary += "<tr>"
                summary += f"<td><b>{operator.name}</b></td>"
                summary += f"<td>{translation_service.tr('district')}: {operator.district}</td>"
                summary += f"<td>{translation_service.tr('category')}: {operator.category}</td>"
                summary += "</tr><tr>"
                summary += (
                    f"<td>{translation_service.tr('country')}: {operator.country}</td>"
                )
                summary += f"<td>{translation_service.tr('province')}: {operator.province}</td>"
                summary += (
                    f"<td>{translation_service.tr('type')}: {operator.type_}</td>"
                )
                summary += "</tr><tr>"
                summary += f"<td>{enabled}</td>"
                summary += f"<td>{translation_service.tr('department')}: {operator.department}</td>"
                summary += f"<td>{translation_service.tr('expiration')}: {operator.expiration_date}</td>"
                summary += "</tr></table>"
                self.show_summary(summary)
            else:
                self.show_suggestions(filtro)
