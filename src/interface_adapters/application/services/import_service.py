"""
Servicio para importar operadores desde un archivo PDF.
Extrae la lógica de negocio fuera de la UI principal.
"""

from application.use_cases.update_operators_from_pdf import update_operators_from_pdf


def import_operators_from_pdf(file_path: str) -> bool:
    """
    Importa operadores desde un archivo PDF usando el updater correspondiente.
    Args:
        file_path (str): Ruta al archivo PDF.
    Returns:
        bool: True si la importación fue exitosa, False en caso contrario.
    """
    return update_operators_from_pdf(file_path)
