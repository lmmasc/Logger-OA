# Script para verificar que todos los códigos de país en ITU_PREFIXES tengan texto en ITU_COUNTRY_NAMES
import re
import ast

PYTHON_FILE = "src/domain/callsign_utils.py"


def extract_dicts(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # ITU_PREFIXES
    match_prefix = re.search(r"ITU_PREFIXES\s*=\s*{(.+?)}", content, re.DOTALL)
    if not match_prefix:
        raise ValueError("ITU_PREFIXES not found")
    dict_prefix_str = "{" + match_prefix.group(1) + "}"
    dict_prefix_str = re.sub(r",\s*}", "}", dict_prefix_str)
    itu_prefixes = ast.literal_eval(dict_prefix_str)
    # ITU_COUNTRY_NAMES
    match_names = re.search(r"ITU_COUNTRY_NAMES\s*=\s*{(.+)}", content, re.DOTALL)
    if not match_names:
        raise ValueError("ITU_COUNTRY_NAMES not found")
    dict_names_str = "{" + match_names.group(1) + "}"
    dict_names_str = re.sub(r",\s*}", "}", dict_names_str)
    itu_country_names = ast.literal_eval(dict_names_str)
    country_codes = set(itu_country_names.keys())
    return itu_prefixes, country_codes


def main():
    itu_prefixes, country_codes = extract_dicts(PYTHON_FILE)
    missing = set()
    for code in set(itu_prefixes.values()):
        if code not in country_codes:
            missing.add(code)
    if missing:
        print("Códigos de país en ITU_PREFIXES sin texto en ITU_COUNTRY_NAMES:")
        for code in sorted(missing):
            print(code)
    else:
        print(
            "Todos los códigos de país en ITU_PREFIXES tienen texto en ITU_COUNTRY_NAMES."
        )


if __name__ == "__main__":
    main()
