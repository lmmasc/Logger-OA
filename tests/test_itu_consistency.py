import os
import re
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
PY_CALLSIGN_UTILS = os.path.join(SRC, "domain/callsign_utils.py")
PY_ITU_PREFIXES = os.path.join(SRC, "domain/itu_prefixes.py")
TS_CALLSIGN_TO_COUNTRY = os.path.join(ROOT, "BaseDocs/callsignToCountry.ts")


def test_prefix_values_have_country_names():
    # Importar diccionarios desde módulos fuente
    itu_prefixes_mod = import_module_from_path("itu_prefixes", PY_ITU_PREFIXES)
    country_names_mod = import_module_from_path(
        "itu_country_names", os.path.join(SRC, "domain/itu_country_names.py")
    )
    ITU_PREFIXES = getattr(itu_prefixes_mod, "ITU_PREFIXES")
    ITU_COUNTRY_NAMES = getattr(country_names_mod, "ITU_COUNTRY_NAMES")

    missing = {
        code for code in set(ITU_PREFIXES.values()) if code not in ITU_COUNTRY_NAMES
    }
    assert (
        missing == set()
    ), "Códigos de país en ITU_PREFIXES sin texto en ITU_COUNTRY_NAMES: " + ", ".join(
        sorted(missing)
    )


def parse_ts_itu_prefixes(ts_path: str) -> set[str]:
    # Extraer objeto ITU_PREFIXES del archivo TS (formato simple clave: 'VAL',)
    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"ITU_PREFIXES:\s*{(.+?)}", content, re.DOTALL)
    if not m:
        raise AssertionError("No se encontró ITU_PREFIXES en el archivo TypeScript")
    body = m.group(1)
    prefixes = set()
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        # Ej: 'AA': 'USA',
        mm = re.match(r"(['\w]+):\s*'([A-Z0-9]+)',?", line)
        if mm:
            key = mm.group(1).strip("'\"")
            prefixes.add(key)
    return prefixes


def parse_py_itu_prefixes(py_path: str) -> set[str]:
    mod = import_module_from_path("itu_prefixes_py", py_path)
    return set(getattr(mod, "ITU_PREFIXES").keys())


def test_ts_prefixes_are_subset_of_python():
    # Verifica que todos los prefijos definidos en el TS existan en Python.
    py_prefixes = parse_py_itu_prefixes(PY_ITU_PREFIXES)
    ts_prefixes = parse_ts_itu_prefixes(TS_CALLSIGN_TO_COUNTRY)
    missing_in_py = sorted(ts_prefixes - py_prefixes)

    # Info diagnóstica (no obliga paridad total entre sets)
    missing_in_ts = sorted(py_prefixes - ts_prefixes)
    if missing_in_ts:
        # No falla: Python puede tener prefijos adicionales que el TS no incluye.
        print(
            "Aviso: prefijos presentes en Python pero no en TS (solo informativo):",
            missing_in_ts[:20],
            "... total:",
            len(missing_in_ts),
        )

    assert (
        not missing_in_py
    ), "Hay prefijos definidos en TS que no existen en Python: " + ", ".join(
        missing_in_py
    )
