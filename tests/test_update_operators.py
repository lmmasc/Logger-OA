import sys
import os
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from src.application.use_cases.update_operators_from_pdf import (
    update_operators_from_pdf,
)


@pytest.mark.integration
def test_update_operators_from_pdf():
    """Prueba la actualización de operadores desde un PDF de ejemplo."""
    demo_pdf = "BaseDocs/396528-radioaficionados_autorizados_al_13ago2025.pdf"
    if not os.path.exists(demo_pdf):
        pytest.skip(f"Archivo de prueba no disponible: {demo_pdf}")
    resultado = update_operators_from_pdf(demo_pdf)
    print("Resultado de la actualización:", resultado)
    assert resultado is not None
