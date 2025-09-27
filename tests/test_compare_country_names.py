import os
import importlib.util


def import_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo importar el archivo: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")


def test_all_prefix_values_have_country_names():
    itu_prefixes_mod = import_module_from_path(
        "itu_prefixes", os.path.join(SRC, "domain/itu_prefixes.py")
    )
    itu_country_names_mod = import_module_from_path(
        "itu_country_names", os.path.join(SRC, "domain/itu_country_names.py")
    )

    ITU_PREFIXES = getattr(itu_prefixes_mod, "ITU_PREFIXES")
    ITU_COUNTRY_NAMES = getattr(itu_country_names_mod, "ITU_COUNTRY_NAMES")

    codes = set(ITU_PREFIXES.values())
    missing = sorted(code for code in codes if code not in ITU_COUNTRY_NAMES)
    assert (
        not missing
    ), "Códigos de país en ITU_PREFIXES sin texto en ITU_COUNTRY_NAMES: " + ", ".join(
        missing
    )
