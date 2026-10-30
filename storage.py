import json
import os
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get('CLASS_PROJECT_DATA_DIR', PROJECT_DIR / 'data'))

COLLECTIONS = {
    'allowances',
    'deductions',
    'departments',
    'employees',
    'payrolls',
    'payslips',
    'positions',
    'salaries',
}


class StorageError(Exception):
    """Raised when saved project data cannot be read safely."""


class DuplicateRecordError(StorageError):
    """Raised when a record would duplicate an existing unique value."""


def collection_path(collection):
    if collection not in COLLECTIONS:
        raise ValueError(f'Unknown data collection: {collection}')
    return DATA_DIR / f'{collection}.json'


def load_records(collection):
    """Load a collection, treating a missing or empty file as an empty list."""
    path = collection_path(collection)
    if not path.exists():
        return []

    try:
        content = path.read_text(encoding='utf-8')
    except OSError as error:
        raise StorageError(f'Could not read {path.name}: {error}') from error

    if not content.strip():
        return []

    try:
        records = json.loads(content)
    except json.JSONDecodeError as error:
        raise StorageError(f'{path.name} contains invalid JSON') from error

    if not isinstance(records, list):
        raise StorageError(f'{path.name} must contain a JSON list')
    if not all(isinstance(record, dict) for record in records):
        raise StorageError(f'Every record in {path.name} must be a JSON object')
    return records


def save_records(collection, records):
    """Write a complete collection through a temporary file."""
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise TypeError('Records must be a list of dictionaries')

    path = collection_path(collection)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix('.json.tmp')

    try:
        temporary_path.write_text(
            json.dumps(records, indent=4),
            encoding='utf-8',
        )
        temporary_path.replace(path)
    except OSError as error:
        raise StorageError(f'Could not save {path.name}: {error}') from error


def append_record(collection, record, unique_fields=None):
    """Append one record while rejecting duplicate unique field values."""
    if not isinstance(record, dict):
        raise TypeError('Record must be a dictionary')

    records = load_records(collection)
    fields = []
    if isinstance(unique_fields, str):
        fields = [unique_fields]
    elif unique_fields:
        fields = list(unique_fields)

    for field in fields:
        if field not in record:
            raise ValueError(f'Record is missing unique field: {field}')

    if fields and any(
        all(saved.get(field) == record[field] for field in fields)
        for saved in records
    ):
        values = ', '.join(f'{field}={record[field]}' for field in fields)
        raise DuplicateRecordError(
            f'Duplicate record in {collection}: {values}'
        )

    records.append(record)
    save_records(collection, records)
    return record
