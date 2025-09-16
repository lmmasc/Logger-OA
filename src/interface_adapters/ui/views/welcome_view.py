from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from translation.translation_service import translation_service
from utils.resources import get_resource_path


class WelcomeView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        # Mensaje de bienvenida arriba
        self.label = QLabel(translation_service.tr("welcome_message"))
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        font = self.label.font()
        font.setPointSize(28)  # Mucho más grande
        font.setBold(True)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # Espaciador superior
        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Logo en el centro
        self.logo_label = QLabel()
        pixmap = QPixmap(get_resource_path("assets/rcp_logo.png"))
        self.logo_label.setPixmap(
            pixmap.scaled(
                400,
                400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Espaciador inferior
        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Mensaje de créditos abajo
        self.credits_label = QLabel(translation_service.tr("credits_message"))
        self.credits_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        )
        credits_font = self.credits_label.font()
        credits_font.setPointSize(14)  # Más grande
        self.credits_label.setFont(credits_font)
        layout.addWidget(self.credits_label)

        self.setLayout(layout)

        translation_service.signal.language_changed.connect(self.retranslate_ui)

    def retranslate_ui(self):
        self.label.setText(translation_service.tr("welcome_message"))
        self.credits_label.setText(translation_service.tr("credits_message"))
