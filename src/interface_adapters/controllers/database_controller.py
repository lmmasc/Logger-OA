"""
Controlador para operaciones de base de datos: backup, restaurar e importar.
"""

from infrastructure.db.backup_restore import (
    create_backup,
    list_backups,
    restore_backup,
    import_from_external_db,
)


class DatabaseController:
    @staticmethod
    def export_database_to_csv(csv_path, translation_service):
        """
        Exporta la base de datos de operadores a un archivo CSV, respetando el orden, formato y traducción visual de la tabla.
        """
        from interface_adapters.controllers.radio_operator_controller import (
            RadioOperatorController,
        )
        import csv

        controller = RadioOperatorController()
        operators = controller.list_operators()
        # Orden y claves de columna como en la tabla
        COLUMN_KEYS = [
            "callsign",
            "name",
            "category",
            "type",
            "region",
            "district",
            "province",
            "department",
            "license",
            "resolution",
            "expiration_date",
            "cutoff_date",
            "enabled",
            "country",
            "updated_at",
        ]
        # Encabezados traducidos
        headers = [translation_service.tr(f"table_header_{key}") for key in COLUMN_KEYS]

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for op in operators:
                row = []
                for key in COLUMN_KEYS:
                    if key == "enabled":
                        value = (
                            translation_service.tr("yes")
                            if getattr(op, key) == 1
                            else translation_service.tr("no")
                        )
                    else:
                        attr = (
                            "type_"
                            if key == "type"
                            else ("license_" if key == "license" else key)
                        )
                        value = getattr(op, attr, "")
                    row.append(str(value))
                writer.writerow(row)

    @staticmethod
    def backup_database():
        """Crea un backup y retorna la ruta o lanza excepción."""
        return create_backup()

    @staticmethod
    def restore_database(backup_filename=None):
        """Restaura la base desde el backup más reciente o uno especificado."""
        backups = list_backups()
        if not backups:
            raise FileNotFoundError("No hay backups disponibles.")
        if backup_filename is None:
            backup_filename = sorted(backups)[-1]
        return restore_backup(backup_filename)

    @staticmethod
    def import_database(external_db_path):
        """Importa operadores desde otra base externa y retorna el número importado."""
        return import_from_external_db(external_db_path)
