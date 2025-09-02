import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from application.use_cases.update_operators_from_pdf import update_operators_from_pdf

# Cambia la ruta al PDF de prueba real si es necesario
demo_pdf = "BaseDocs/396528-radioaficionados_autorizados_al_13ago2025.pdf"

result = update_operators_from_pdf(demo_pdf)
print("Resultado de la actualización:", result)
