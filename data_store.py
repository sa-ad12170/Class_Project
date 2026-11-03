import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data.json"
SECTIONS = ("departments", "salary_scales", "allowances", "payroll_roster", "payrolls")


def _load_data():
    """Load the JSON object and make sure its expected sections are available."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if not isinstance(data, dict):
        data = {}

    for section in SECTIONS:
        if not isinstance(data.get(section), list):
            data[section] = []
    return data


def load_records(section):
    """Return one list from data.json, such as departments or payrolls."""
    if section not in SECTIONS:
        raise ValueError(f"Unknown data section: {section}")
    return _load_data()[section]


def save_records(section, records):
    """Replace one list in data.json while preserving all other lists."""
    if section not in SECTIONS:
        raise ValueError(f"Unknown data section: {section}")
    if not isinstance(records, list):
        raise TypeError("Saved records must be a list.")

    data = _load_data()
    data[section] = records
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")
