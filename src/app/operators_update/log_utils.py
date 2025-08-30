"""
Utilidades para logging y reportes de cambios en la actualización de operadores.
"""


def log_update(summary):
    """
    Registra y muestra un resumen de la actualización de operadores.
    """
    print("Resumen de actualización de operadores:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
