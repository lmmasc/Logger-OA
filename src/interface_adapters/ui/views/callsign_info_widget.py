from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QScrollArea,
    QLabel,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, Qt
from translation.translation_service import translation_service
from utils.text import get_filtered_operators


class CallsignInfoWidget(QWidget):
    suggestionSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._showing_suggestions = False
        self._current_callsign = ""
        self.layout = QVBoxLayout(self)
        self.group_box = QGroupBox("", self)
        self.group_box.setStyleSheet(
            "QGroupBox { padding: 2px; margin-top: 10px; min-height: 110px; }"
        )
        self.summary_label = QLabel("", self.group_box)
        self.summary_label.setWordWrap(True)
        summary_font = QFont()
        summary_font.setPointSize(20)
        self.summary_label.setFont(summary_font)
        self.summary_label.setMinimumHeight(40)
        self.summary_scroll = QScrollArea(self.group_box)
        self.summary_scroll.setWidgetResizable(True)
        self.summary_scroll.setWidget(self.summary_label)
        self.summary_scroll.setFixedHeight(90)
        self.suggestion_list = QListWidget(self.group_box)
        self.suggestion_list.setFixedHeight(90)
        self.suggestion_list.setViewMode(QListWidget.IconMode)
        self.suggestion_list.setFlow(QListWidget.LeftToRight)
        self.suggestion_list.setWrapping(True)
        self.suggestion_list.setResizeMode(QListWidget.Adjust)
        self.suggestion_list.setSpacing(5)
        self.suggestion_list.setStyleSheet("QListWidget::item { color: #1976d2; }")
        self.suggestion_list.hide()
        self.suggestion_list.itemClicked.connect(self._on_suggestion_clicked)
        group_layout = QVBoxLayout(self.group_box)
        group_layout.setContentsMargins(2, 2, 2, 2)
        group_layout.addWidget(self.summary_scroll)
        group_layout.addWidget(self.suggestion_list)
        self.group_box.setLayout(group_layout)
        self.layout.addWidget(self.group_box)
        self.setLayout(self.layout)
        self.retranslate_ui()

    def show_summary(self, text):
        print(f"[CallsignInfoWidget] show_summary called with text: {text[:60]}")
        self._showing_suggestions = False
        self.suggestion_list.hide()
        self.summary_scroll.show()
        self.summary_label.setText(text)
        self.group_box.setTitle(translation_service.tr("callsign_summary"))

    def show_suggestions(self, filtro):
        self._showing_suggestions = True
        self.summary_scroll.hide()
        self.suggestion_list.show()
        self.suggestion_list.clear()
        if not filtro or len(filtro) < 2:
            operadores = []
        else:
            operadores = get_filtered_operators(filtro)
        for op in operadores:
            item = QListWidgetItem(op.callsign)
            font = QFont()
            font.setPointSize(18)
            font.setBold(True)
            item.setFont(font)
            if op.name:
                item.setToolTip(op.name)
            self.suggestion_list.addItem(item)
        self.group_box.setTitle(translation_service.tr("suggestions_label"))

    def _on_suggestion_clicked(self, item):
        self.suggestionSelected.emit(item.text())

    def retranslate_ui(self):
        if self._showing_suggestions:
            self.group_box.setTitle(translation_service.tr("suggestions_label"))
        else:
            self.group_box.setTitle(translation_service.tr("callsign_summary"))

    def update_info(self, text):
        filtro = text.strip().upper()
        if len(filtro) < 2:
            # Menos de 2 caracteres: título sugerencias, lista vacía
            self.show_suggestions("")
        else:
            from infrastructure.repositories.sqlite_radio_operator_repository import (
                SqliteRadioOperatorRepository,
            )

            repo = SqliteRadioOperatorRepository()
            operadores = get_filtered_operators(filtro)
            # Buscar match único y exacto
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
                # 2+ caracteres: título sugerencias, lista filtrada (puede estar vacía)
                self.show_suggestions(filtro)
