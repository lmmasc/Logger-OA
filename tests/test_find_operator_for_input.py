import os
import sqlite3
import time
import types
import importlib
import pytest

# We will import the function after preparing the temporary DB and monkeypatching get_database_path


def _init_temp_db(tmp_path):
    db_path = os.path.join(tmp_path, "loggeroa_test.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS radio_operators (
            callsign TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            type TEXT,
            region TEXT,
            district TEXT,
            province TEXT,
            department TEXT,
            license TEXT,
            resolution TEXT,
            expiration_date INTEGER,
            cutoff_date INTEGER,
            enabled INTEGER,
            country TEXT,
            updated_at INTEGER
        )
        """
    )
    now = int(time.time())
    rows = [
        (
            "OA4BAU",
            "Juan Perez",
            "G",
            "H",
            "LIM",
            "Lima",
            "Lima",
            "Lima",
            "123",
            "R-1",
            None,
            None,
            1,
            "PER",
            now,
        ),
        (
            "CE3ABC",
            "Maria",
            "G",
            "H",
            "REG",
            "Dist",
            "Prov",
            "Dept",
            "",
            "",
            None,
            None,
            1,
            "CHL",
            now,
        ),
        ("EA4", "Pepe", "G", "H", "MAD", "", "", "", "", "", None, None, 1, "ESP", now),
    ]
    cur.executemany(
        "INSERT INTO radio_operators (callsign, name, category, type, region, district, province, department, license, resolution, expiration_date, cutoff_date, enabled, country, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        rows,
    )
    conn.commit()
    conn.close()
    return db_path


def test_find_operator_for_input_base(monkeypatch, tmp_path):
    db_path = _init_temp_db(tmp_path)
    # Monkeypatch get_database_path
    from src.infrastructure.db import queries as q
    from src.config import paths as paths_mod

    # Also patch non-namespaced imports used at runtime
    import infrastructure.db.queries as q2
    import config.paths as paths_mod2

    monkeypatch.setattr(q, "get_database_path", lambda: db_path)
    monkeypatch.setattr(q2, "get_database_path", lambda: db_path)
    monkeypatch.setattr(
        paths_mod, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    monkeypatch.setattr(
        paths_mod2, "get_database_path", lambda filename="loggeroa.db": db_path
    )

    # Import after monkeypatch
    mod = importlib.import_module("src.application.use_cases.operator_management")

    op = mod.find_operator_for_input("OA4BAU")
    assert op is not None
    assert op.callsign == "OA4BAU"
    assert op.name == "Juan Perez"


def test_find_operator_for_input_with_prefix(monkeypatch, tmp_path):
    db_path = _init_temp_db(tmp_path)
    from src.infrastructure.db import queries as q
    from src.config import paths as paths_mod
    import infrastructure.db.queries as q2
    import config.paths as paths_mod2

    monkeypatch.setattr(q, "get_database_path", lambda: db_path)
    monkeypatch.setattr(q2, "get_database_path", lambda: db_path)
    monkeypatch.setattr(
        paths_mod, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    monkeypatch.setattr(
        paths_mod2, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    mod = importlib.import_module("src.application.use_cases.operator_management")

    # Should resolve base OA4BAU from CE3/OA4BAU
    op = mod.find_operator_for_input("CE3/OA4BAU")
    assert op is not None
    assert op.callsign == "OA4BAU"


def test_find_operator_for_input_with_suffix(monkeypatch, tmp_path):
    db_path = _init_temp_db(tmp_path)
    from src.infrastructure.db import queries as q
    from src.config import paths as paths_mod
    import infrastructure.db.queries as q2
    import config.paths as paths_mod2

    monkeypatch.setattr(q, "get_database_path", lambda: db_path)
    monkeypatch.setattr(q2, "get_database_path", lambda: db_path)
    monkeypatch.setattr(
        paths_mod, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    monkeypatch.setattr(
        paths_mod2, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    mod = importlib.import_module("src.application.use_cases.operator_management")

    # Suffix should be ignored for lookup
    op = mod.find_operator_for_input("OA4BAU/M")
    assert op is not None
    assert op.callsign == "OA4BAU"


def test_find_operator_for_input_prefix_and_suffix(monkeypatch, tmp_path):
    db_path = _init_temp_db(tmp_path)
    from src.infrastructure.db import queries as q
    from src.config import paths as paths_mod
    import infrastructure.db.queries as q2
    import config.paths as paths_mod2

    monkeypatch.setattr(q, "get_database_path", lambda: db_path)
    monkeypatch.setattr(q2, "get_database_path", lambda: db_path)
    monkeypatch.setattr(
        paths_mod, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    monkeypatch.setattr(
        paths_mod2, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    mod = importlib.import_module("src.application.use_cases.operator_management")

    op = mod.find_operator_for_input("CE3/OA4BAU/M")
    assert op is not None
    assert op.callsign == "OA4BAU"


def test_find_operator_for_input_no_match(monkeypatch, tmp_path):
    db_path = _init_temp_db(tmp_path)
    from src.infrastructure.db import queries as q
    from src.config import paths as paths_mod
    import infrastructure.db.queries as q2
    import config.paths as paths_mod2

    monkeypatch.setattr(q, "get_database_path", lambda: db_path)
    monkeypatch.setattr(q2, "get_database_path", lambda: db_path)
    monkeypatch.setattr(
        paths_mod, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    monkeypatch.setattr(
        paths_mod2, "get_database_path", lambda filename="loggeroa.db": db_path
    )
    mod = importlib.import_module("src.application.use_cases.operator_management")

    op = mod.find_operator_for_input("ZZ9/PLURAL/Z")
    assert op is None
