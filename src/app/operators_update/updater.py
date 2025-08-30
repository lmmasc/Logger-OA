"""
Orquestador del proceso de actualización de operadores desde PDF.
"""

from .pdf_extractor import extract_operators_from_pdf
from .data_normalizer import normalize_operator_data
from .db_integrator import integrate_operators_to_db


def update_operators_from_pdf(pdf_path):
    """
    Ejecuta el flujo completo de extracción, normalización e integración.
    """
    raw_data = extract_operators_from_pdf(pdf_path)
    normalized_data = normalize_operator_data(raw_data)
    result = integrate_operators_to_db(normalized_data)
    return result
