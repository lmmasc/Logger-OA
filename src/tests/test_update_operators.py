from infrastructure.operators_update.updater import update_operators_from_pdf

# Cambia la ruta al PDF de prueba real si es necesario
demo_pdf = "BaseDocs/396528-radioaficionados_autorizados_al_13ago2025.pdf"

result = update_operators_from_pdf(demo_pdf)
print("Resultado de la actualización:", result)
