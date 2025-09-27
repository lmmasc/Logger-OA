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


def parse_ts_itu_prefixes(ts_path: str) -> set[str]:
    with open(ts_path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"ITU_PREFIXES:\s*{(.+?)}", content, re.DOTALL)
    if not m:
        raise AssertionError("No se encontró ITU_PREFIXES en TypeScript")
    body = m.group(1)
    prefixes = set()
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        mm = re.match(r"(['\w]+):\s*'([A-Z0-9]+)',?", line)
        if mm:
            key = mm.group(1).strip("'\"")
            prefixes.add(key)
    return prefixes


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
TS_FILE = os.path.join(ROOT, "BaseDocs/callsignToCountry.ts")


def test_ts_prefixes_are_subset_of_python():
    itu_prefixes_mod = import_module_from_path(
        "itu_prefixes", os.path.join(SRC, "domain/itu_prefixes.py")
    )
    ITU_PREFIXES = getattr(itu_prefixes_mod, "ITU_PREFIXES")
    py_prefixes = set(ITU_PREFIXES.keys())
    ts_prefixes = parse_ts_itu_prefixes(TS_FILE)
    missing_in_py = sorted(ts_prefixes - py_prefixes)
    assert (
        not missing_in_py
    ), "Hay prefijos definidos en TS que no existen en Python: " + ", ".join(
        missing_in_py
    )
