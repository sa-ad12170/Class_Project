"""Department persistence helpers and compatibility import."""

from data_store import load_records, save_records
from oop_prac import Department, SalaryScale

DEPARTMENTS_SECTION = "departments"
DEFAULT_DEPARTMENTS = ("IT", "Accounts", "Security")


def load_departments(scale=None):
    records = load_records(DEPARTMENTS_SECTION)
    scale = SalaryScale.load() if scale is None else scale
    departments = [Department.from_dict(record, scale) for record in records
                   if isinstance(record, dict)]
    existing = {department.departmentname.casefold() for department in departments}
    for name in DEFAULT_DEPARTMENTS:
        if name.casefold() not in existing:
            departments.append(Department(f"dept{len(departments) + 1:03d}", name))
    return departments


def save_departments(departments):
    save_records(DEPARTMENTS_SECTION,
                 [department.to_dict() for department in departments])
