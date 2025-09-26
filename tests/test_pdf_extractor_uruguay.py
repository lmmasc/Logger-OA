import sys, os
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from infrastructure.pdf.pdf_extractor import extract_operators_from_pdf


@pytest.mark.integration
def test_extract_uruguay_pdf_basic():
    pdf = "BaseDocs/Nomina CX Vigentes julio 2025.pdf"
    ops = extract_operators_from_pdf(pdf)
    assert isinstance(ops, list)
    assert len(ops) > 10  # debería extraer varias decenas
    sample = ops[0]
    # Campos esenciales
    assert "callsign" in sample and sample["callsign"].startswith("CX")
    assert "name" in sample and len(sample["name"]) > 0
    assert "category" in sample and sample["category"] in {
        "INICIAL",
        "GENERAL",
        "SUPERIOR",
    }
    assert "expiration_date" in sample and isinstance(sample["expiration_date"], int)
    assert "country" in sample and sample["country"] == "URY"
