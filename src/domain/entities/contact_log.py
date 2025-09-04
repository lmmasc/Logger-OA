from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid
import re


@dataclass
class ContactLog:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operator: str = ""
    start_time: str = ""
    end_time: str = ""
    contacts: List[Any] = field(default_factory=list)  # Se especializa en subclases
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def add_contact(self, contact):
        if self.is_duplicate_contact(contact):
            raise ValueError("Contacto duplicado: ya existe un contacto con el mismo indicativo y hora.")
        if not self.is_valid_callsign(contact.callsign):
            raise ValueError(f"Indicativo inválido: {contact.callsign}")
        if hasattr(contact, 'qtr_utc') and not self.is_valid_time(contact.qtr_utc):
            raise ValueError(f"Hora UTC inválida: {contact.qtr_utc}")
        self.contacts.append(contact)

    def remove_contact(self, contact):
        self.contacts.remove(contact)

    def is_duplicate_contact(self, new_contact) -> bool:
        # Considera duplicado si hay mismo indicativo y hora (qtr_utc o time_utc)
        for c in self.contacts:
            if hasattr(c, 'callsign') and hasattr(new_contact, 'callsign') and c.callsign == new_contact.callsign:
                time_field = getattr(c, 'qtr_utc', getattr(c, 'time_utc', None))
                new_time_field = getattr(new_contact, 'qtr_utc', getattr(new_contact, 'time_utc', None))
                if time_field and new_time_field and time_field == new_time_field:
                    return True
        return False

    @staticmethod
    def is_valid_callsign(callsign: str) -> bool:
        # Validación simple de indicativo (puede mejorarse según país)
        return bool(re.match(r'^[A-Z0-9]{3,}$', callsign.upper()))

    @staticmethod
    def is_valid_time(timestr: str) -> bool:
        # Espera formato HHMM o HH:MM
        return bool(re.match(r'^(\d{4}|\d{2}:\d{2})$', timestr))
