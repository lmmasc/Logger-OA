import json
import sqlite3
from datetime import datetime, timezone

from application.use_cases.open_log import open_log
from application.use_cases.log_file_format import CURRENT_LOG_FILE_FORMAT_VERSION
from config.paths import format_timestamp_local
from interface_adapters.ui.view_manager import LogType
from utils.datetime import parse_utc_timestamp


def _create_legacy_log_db(db_path, log_type=LogType.OPERATION_LOG.value):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE logs (
                id TEXT PRIMARY KEY,
                type TEXT,
                operator TEXT,
                start_time INTEGER,
                end_time INTEGER,
                metadata TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE contacts (
                id TEXT PRIMARY KEY,
                log_id TEXT,
                data TEXT,
                FOREIGN KEY(log_id) REFERENCES logs(id)
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO logs (id, type, operator, start_time, end_time, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "log-1",
                log_type,
                "OA4TEST",
                "2025-09-19_21-15-02",
                "2025-09-19_22-00-00",
                json.dumps({"contest_name_key": "contest_world_radio_day"}),
            ),
        )
        cursor.execute(
            """
            INSERT INTO contacts (id, log_id, data)
            VALUES (?, ?, ?)
            """,
            (
                "contact-1",
                "log-1",
                json.dumps(
                    {
                        "callsign": "OA4ABC",
                        "timestamp": "2025-09-19_21-15-02",
                    }
                ),
            ),
        )
        conn.commit()


def test_parse_utc_timestamp_accepts_legacy_local_string():
    parsed = parse_utc_timestamp("2025-09-19_21-15-02")
    expected = int(
        datetime(2025, 9, 20, 2, 15, 2, tzinfo=timezone.utc).timestamp()
    )
    assert parsed == expected


def test_open_log_accepts_legacy_string_timestamps(tmp_path):
    db_path = tmp_path / "legacy-log.sqlite"
    _create_legacy_log_db(str(db_path), log_type=LogType.CONTEST_LOG.value)

    log = open_log(str(db_path))

    assert log.operator == "OA4TEST"
    assert log.start_time == parse_utc_timestamp("2025-09-19_21-15-02")
    assert log.end_time == parse_utc_timestamp("2025-09-19_22-00-00")
    assert len(log.contacts) == 1
    assert log.contacts[0]["timestamp"] == parse_utc_timestamp("2025-09-19_21-15-02")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT start_time, end_time FROM logs WHERE id = ?", ("log-1",))
        persisted_log_row = cursor.fetchone()
        cursor.execute("SELECT metadata FROM logs WHERE id = ?", ("log-1",))
        persisted_metadata = json.loads(cursor.fetchone()[0])
        cursor.execute("SELECT data FROM contacts WHERE id = ?", ("contact-1",))
        persisted_contact_data = json.loads(cursor.fetchone()[0])
        cursor.execute("PRAGMA user_version")
        persisted_user_version = cursor.fetchone()[0]

    assert persisted_log_row == (
        parse_utc_timestamp("2025-09-19_21-15-02"),
        parse_utc_timestamp("2025-09-19_22-00-00"),
    )
    assert persisted_contact_data["timestamp"] == parse_utc_timestamp(
        "2025-09-19_21-15-02"
    )
    assert persisted_contact_data["id"] == "contact-1"
    assert persisted_metadata["contest_name_key"] == "contest_world_radio_day"
    assert (
        persisted_metadata["file_format_version"]
        == CURRENT_LOG_FILE_FORMAT_VERSION
    )
    assert persisted_user_version == CURRENT_LOG_FILE_FORMAT_VERSION


def test_format_timestamp_local_accepts_legacy_string_timestamp():
    assert format_timestamp_local("2025-09-19_21-15-02") == "2025-09-19_21-15-02"