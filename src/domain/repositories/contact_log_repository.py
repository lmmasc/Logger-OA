import sqlite3
from typing import Any, List, Optional
from ..entities.contact_log import ContactLog


class ContactLogRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    operator TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    metadata TEXT
                )
            """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id TEXT PRIMARY KEY,
                    log_id TEXT,
                    data TEXT,
                    FOREIGN KEY(log_id) REFERENCES logs(id)
                )
            """
            )
            conn.commit()

    def save_log(self, log: ContactLog, log_type_str: str):
        import json

        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT OR REPLACE INTO logs (id, type, operator, start_time, end_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    log.id,
                    log_type_str,  # Guarda el string del tipo de log
                    log.operator,
                    log.start_time,
                    log.end_time,
                    json.dumps(log.metadata or {}),
                ),
            )
            conn.commit()

    def get_log(self, log_id: str) -> Optional[ContactLog]:
        # Implementar: cargar y deserializar log según tipo
        pass

    def delete_log(self, log_id: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM logs WHERE id = ?", (log_id,))
            c.execute("DELETE FROM contacts WHERE log_id = ?", (log_id,))
            conn.commit()

    def save_contact(self, log_id: str, contact: Any):
        import json, uuid

        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            contact_id = getattr(contact, "id", str(uuid.uuid4()))
            c.execute(
                """
                INSERT OR REPLACE INTO contacts (id, log_id, data)
                VALUES (?, ?, ?)
            """,
                (contact_id, log_id, json.dumps(contact.__dict__)),
            )
            conn.commit()

    def get_contacts(self, log_id: str) -> List[Any]:
        import json

        contacts = []
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT data FROM contacts WHERE log_id = ?", (log_id,))
            rows = c.fetchall()
            for row in rows:
                data = row[0]
                try:
                    contact_dict = json.loads(data)
                    contacts.append(contact_dict)
                except Exception:
                    continue
        return contacts

    def delete_contact(self, contact_id: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()

    def update_contact(self, contact_id: str, contact: Any):
        import json

        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """
                UPDATE contacts SET data = ? WHERE id = ?
                """,
                (json.dumps(contact.__dict__), contact_id),
            )
            conn.commit()
