"""writes records down """


import json
from pathlib import Path
from typing import Any

from controls import for_storage

LOG_FILE = Path(__file__).parent / "appointment_log.jsonl"


def save_record(record: dict) -> None:
    """ redact personal data before storing an appointment record """

    safe_record = for_storage(record)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(safe_record) + "\n")


def read_saved_records() -> list:
    """Read previously saved records."""
    if not LOG_FILE.exists():
        return []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]