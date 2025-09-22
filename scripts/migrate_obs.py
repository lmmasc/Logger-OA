import sqlite3
import sys
import os
import json


def migrate_observations_to_obs(db_path):
    if not os.path.isfile(db_path):
        print(f"Archivo no encontrado: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Asume que la tabla de contactos se llama 'contacts' y el campo JSON/texto se llama 'data'
    cursor.execute("SELECT id, data FROM contacts")
    rows = cursor.fetchall()
    updated = 0

    for contact_id, data in rows:
        try:
            contact = json.loads(data)
        except Exception:
            continue
        if "observations" in contact:
            contact["obs"] = contact.pop("observations")
            new_data = json.dumps(contact, ensure_ascii=False)
            cursor.execute(
                "UPDATE contacts SET data = ? WHERE id = ?", (new_data, contact_id)
            )
            updated += 1

    conn.commit()
    conn.close()
    print(f"Actualizados {updated} registros en {db_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python migrate_obs.py /ruta/al/archivo.sqlite")
    else:
        migrate_observations_to_obs(sys.argv[1])
