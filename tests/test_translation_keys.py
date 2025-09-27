import unittest

import importlib.util
import os


def import_dict_from_py(file_path, dict_name):
    spec = importlib.util.spec_from_file_location(dict_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo importar el archivo: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, dict_name)


SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
EN_PATH = os.path.join(SRC, "translation/en/all_keys.py")
ES_PATH = os.path.join(SRC, "translation/es/all_keys.py")

ALL_TRANSLATIONS_EN = import_dict_from_py(EN_PATH, "ALL_KEYS_TRANSLATIONS")
ALL_TRANSLATIONS_ES = import_dict_from_py(ES_PATH, "ALL_KEYS_TRANSLATIONS")


class TestTranslationKeys(unittest.TestCase):
    def test_keys_match(self):
        en_keys = set(ALL_TRANSLATIONS_EN.keys())
        es_keys = set(ALL_TRANSLATIONS_ES.keys())
        missing_in_es = en_keys - es_keys
        missing_in_en = es_keys - en_keys
        if missing_in_es:
            print("Claves faltantes en español:", missing_in_es)
        if missing_in_en:
            print("Claves faltantes en inglés:", missing_in_en)
        self.assertEqual(missing_in_es, set(), f"Faltan en español: {missing_in_es}")
        self.assertEqual(missing_in_en, set(), f"Faltan en inglés: {missing_in_en}")


if __name__ == "__main__":
    unittest.main()
