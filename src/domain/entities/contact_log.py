from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid


@dataclass
class ContactLog:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operator: str = ""
    start_time: str = ""
    end_time: str = ""
    contacts: List[Any] = field(default_factory=list)  # Se especializa en subclases
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def add_contact(self, contact):
        self.contacts.append(contact)

    def remove_contact(self, contact):
        self.contacts.remove(contact)

    # Métodos de validación y lógica común pueden agregarse aquí
