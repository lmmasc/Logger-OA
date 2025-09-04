"""
Reglas específicas para concursos.
Documentación en español.
"""


class ContestRules:
    """
    Clase para reglas de negocio específicas de concursos.
    """

    @staticmethod
    def validate_exchange(contact) -> list:
        errors = []
        # Ejemplo: el intercambio recibido y enviado no deben estar vacíos
        if not getattr(contact, "exchange_received", None):
            errors.append("Missing received exchange.")
        if not getattr(contact, "exchange_sent", None):
            errors.append("Missing sent exchange.")
        # Aquí se pueden agregar más reglas específicas según el reglamento
        return errors

    @staticmethod
    def validate_band(contact, allowed_bands=None) -> list:
        errors = []
        if allowed_bands:
            band = getattr(contact, "band", None)
            if band and band not in allowed_bands:
                errors.append(f"Band not allowed: {band}")
        return errors

    @staticmethod
    def validate(contact, contacts, allowed_bands=None) -> list:
        """
        Ejecuta todas las validaciones específicas de concursos.
        """
        errors = []
        errors += ContestRules.validate_exchange(contact)
        errors += ContestRules.validate_band(contact, allowed_bands)
        # Aquí se pueden agregar más validaciones según el reglamento
        return errors
