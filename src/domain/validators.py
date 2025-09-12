"""
Validador genérico para logs y contactos.
Documentación en español.
"""

import re


class LogValidator:
    """
    Clase base para validaciones genéricas de logs y contactos.
    """

    @staticmethod
    def is_valid_callsign(callsign: str) -> bool:
        # Validación simple de indicativo (puede mejorarse según país)
        return bool(re.match(r"^[A-Z0-9]{3,}$", callsign.upper()))

    @staticmethod
    def is_valid_time(timestr: str) -> bool:
        # Espera formato HHMM o HH:MM
        return bool(re.match(r"^(\d{4}|\d{2}:\d{2})$", timestr))

    @staticmethod
    def is_duplicate_contact(new_contact, contacts) -> bool:
        # Considera duplicado si hay mismo indicativo y hora (qtr_utc o time_utc)
        for c in contacts:
            if (
                hasattr(c, "callsign")
                and hasattr(new_contact, "callsign")
                and c.callsign == new_contact.callsign
            ):
                time_field = getattr(c, "qtr_utc", getattr(c, "time_utc", None))
                new_time_field = getattr(
                    new_contact, "qtr_utc", getattr(new_contact, "time_utc", None)
                )
                if time_field and new_time_field and time_field == new_time_field:
                    return True
        return False

    @staticmethod
    def validate_contact(contact, contacts) -> list:
        """
        Realiza todas las validaciones y retorna una lista de errores (vacía si todo es válido).
        """
        errors = []
        if LogValidator.is_duplicate_contact(contact, contacts):
            errors.append("Duplicate contact: same callsign and time.")
        if not LogValidator.is_valid_callsign(contact.callsign):
            errors.append(f"Invalid callsign: {contact.callsign}")
        time_field = getattr(contact, "qtr_utc", getattr(contact, "time_utc", None))
        if time_field and not LogValidator.is_valid_time(time_field):
            errors.append(f"Invalid time format: {time_field}")
        # Validar RS_RX y RS_TX
        rs_rx = getattr(contact, "rs_rx", None)
        rs_tx = getattr(contact, "rs_tx", None)
        if not rs_rx or rs_rx.strip() == "":
            errors.append("Missing RS_RX.")
        if not rs_tx or rs_tx.strip() == "":
            errors.append("Missing RS_TX.")
        return errors
