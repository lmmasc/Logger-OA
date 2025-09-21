import re
import ast

# Paths to files
PYTHON_FILE = "src/domain/callsign_utils.py"
TYPESCRIPT_FILE = "BaseDocs/callsignToCountry.ts"


def extract_python_prefixes(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find ITU_PREFIXES dict
    match = re.search(r"ITU_PREFIXES\s*=\s*{(.+?)}", content, re.DOTALL)
    if not match:
        raise ValueError("ITU_PREFIXES not found")
    dict_str = "{" + match.group(1) + "}"
    # Replace trailing commas and parse
    dict_str = re.sub(r",\s*}", "}", dict_str)
    # Use ast.literal_eval for safe parsing
    py_dict = ast.literal_eval(dict_str)
    return set(py_dict.keys())


def extract_ts_prefixes(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find ITU_PREFIXES object
    match = re.search(r"ITU_PREFIXES:\s*{(.+?)}", content, re.DOTALL)
    if not match:
        raise ValueError("ITU_PREFIXES not found")
    dict_str = match.group(1)
    # Parse lines
    ts_dict = {}
    for line in dict_str.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        m = re.match(r"(['\w]+'):\s*'([A-Z]+)',?", line)
        if m:
            key, val = m.group(1), m.group(2)
            ts_dict[key] = val
    return set(ts_dict.keys())


def main():
    py_prefixes = extract_python_prefixes(PYTHON_FILE)
    ts_prefixes = extract_ts_prefixes(TYPESCRIPT_FILE)
    missing_in_py = sorted(ts_prefixes - py_prefixes)
    missing_in_ts = sorted(py_prefixes - ts_prefixes)
    print("Prefijos en TypeScript pero NO en Python:")
    for p in missing_in_py:
        print(p)
    print("\nPrefijos en Python pero NO en TypeScript:")
    for p in missing_in_ts:
        print(p)


if __name__ == "__main__":
    main()
