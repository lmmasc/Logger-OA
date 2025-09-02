"""
Controlador para la gestión de operadores de radio.
Actúa como intermediario entre la UI y los servicios/casos de uso.
"""

from app.services.radio_operator_service import RadioOperatorService
from infrastructure.repositories.sqlite_radio_operator_repository import (
    SqliteRadioOperatorRepository,
)


class RadioOperatorController:
    def __init__(self):
        repo = SqliteRadioOperatorRepository()
        self.service = RadioOperatorService(repo)

    def list_operators(self):
        return self.service.list_operators()

    # Métodos adicionales para agregar, actualizar, etc. pueden agregarse aquí
