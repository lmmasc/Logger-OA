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
