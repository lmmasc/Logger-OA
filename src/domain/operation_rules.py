"""
Reglas específicas para operativos.
Documentación en español.
"""


class OperationRules:
    """
    Clase para reglas de negocio específicas de operativos.
    """

    @staticmethod
    def validate_station(contact) -> list:
        errors = []
        if not getattr(contact, "station", None):
            errors.append("Missing station.")
        # Aquí se pueden agregar más reglas específicas
        return errors

    @staticmethod
    def validate_power(contact) -> list:
        errors = []
        power = getattr(contact, "power", None)
        if power and not power.isdigit():
            errors.append(f"Invalid power value: {power}")
        return errors

    @staticmethod
    def validate(contact, contacts) -> list:
        """
        Ejecuta todas las validaciones específicas de operativos.
        """
        errors = []
        errors += OperationRules.validate_station(contact)
        errors += OperationRules.validate_power(contact)
        # Aquí se pueden agregar más validaciones
        return errors
