"""
Caso de uso: Importar operadores desde un archivo PDF.
Extrae la lógica de negocio fuera de la UI principal.
"""

from application.interfaces.operators_update import OperatorsUpdater


def import_operators_from_pdf(file_path: str, updater: OperatorsUpdater) -> bool:
    """
    Importa operadores desde un archivo PDF usando el updater correspondiente.
    Args:
        file_path (str): Ruta al archivo PDF.
        updater (OperatorsUpdater): Implementación del actualizador.
    Returns:
        bool: True si la importación fue exitosa, False en caso contrario.
    """
    return updater.update_operators_from_pdf(file_path)
