from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from oop_prac import Allowance, Deductions, Employee, Payslip
from storage import (
    DuplicateRecordError,
    StorageError,
    append_record,
    load_records,
)


PROJECT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = PROJECT_DIR / 'frontend'

app = FastAPI(
    title='Class Project Payroll API',
    description='A small employee and payroll API backed by local JSON files.',
    version='1.0.0',
)
app.mount('/static', StaticFiles(directory=FRONTEND_DIR), name='static')


class EmployeeCreate(BaseModel):
    employee_id: str = Field(min_length=1, max_length=40)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    birth_year: int = Field(ge=1900, le=datetime.today().year)
    department: str = Field(min_length=1, max_length=80)
    gender: str = Field(min_length=1, max_length=30)
    employment_status: str = Field(min_length=1, max_length=30)
    contact: str = Field(min_length=1, max_length=50)
    village: str = Field(min_length=1, max_length=80)
    city: str = Field(min_length=1, max_length=80)
    position: str = Field(min_length=1, max_length=80)

    @field_validator(
        'employee_id',
        'first_name',
        'last_name',
        'department',
        'gender',
        'employment_status',
        'contact',
        'village',
        'city',
        'position',
    )
    @classmethod
    def strip_required_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('Value cannot be blank')
        return value


class PayrollCalculation(BaseModel):
    base_salary: float = Field(ge=0)
    allowance_rate: float = Field(default=0, ge=0, le=100)
    deduction_rate: float = Field(default=0, ge=0, le=100)
    hours_worked: float = Field(default=0, ge=0)


class PayslipCreate(PayrollCalculation):
    payslip_id: str = Field(min_length=1, max_length=40)
    employee_id: str = Field(min_length=1, max_length=40)
    payroll_id: str | None = Field(default=None, max_length=40)

    @field_validator('payslip_id', 'employee_id', 'payroll_id')
    @classmethod
    def strip_identifiers(cls, value):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError('Value cannot be blank')
        return value


def get_records(collection):
    try:
        return load_records(collection)
    except StorageError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


def save_api_record(collection, record, unique_fields):
    try:
        append_record(collection, record, unique_fields)
    except DuplicateRecordError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except StorageError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    return record


def calculate_pay(payload):
    allowance = Allowance(
        'preview-allowance',
        'preview-payroll',
        'preview-employee',
        'Allowance',
        payload.allowance_rate,
    )
    deduction = Deductions(
        'preview-deduction',
        'Deduction',
        payload.deduction_rate,
        'preview-payroll',
        'preview-employee',
        payload.base_salary,
    )
    allowance_amount = allowance.compute_amount(payload.base_salary)
    deduction_amount = deduction.get_amount()
    payslip = Payslip(
        'preview-payslip',
        'Preview Employee',
        deduction_amount,
        allowance_amount,
        payload.hours_worked,
    )
    payslip.set_gross(payload.base_salary)
    return {
        'base_salary': payload.base_salary,
        'allowance_rate': payload.allowance_rate,
        'allowance_amount': allowance_amount,
        'deduction_rate': payload.deduction_rate,
        'deduction_amount': deduction_amount,
        'gross': payslip.get_gross(),
        'net': payslip.get_net(),
        'hours_worked': payload.hours_worked,
    }


@app.get('/', include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / 'index.html')


@app.get('/api/health')
def health():
    return {'status': 'ok'}


@app.get('/api/dashboard')
def dashboard():
    employees = get_records('employees')
    departments = get_records('departments')
    payrolls = get_records('payrolls')
    payslips = get_records('payslips')
    positions = get_records('positions')
    return {
        'stats': {
            'employees': len(employees),
            'departments': len(departments) or 2,
            'positions': len(positions),
            'payrolls': len(payrolls),
            'payslips': len(payslips),
            'total_net_pay': sum(item.get('net', 0) for item in payslips),
        },
        'recent_payslips': list(reversed(payslips[-5:])),
    }


@app.get('/api/employees')
def list_employees():
    return get_records('employees')


@app.post('/api/employees', status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate):
    employee = Employee(
        payload.employee_id,
        payload.first_name,
        payload.last_name,
        payload.birth_year,
        payload.department,
        payload.gender,
        payload.employment_status,
        payload.contact,
        payload.village,
        payload.city,
        payload.position,
    )
    record = {
        'employee_id': employee.id,
        'first_name': employee.firstname,
        'last_name': employee.lastname,
        'birth_year': employee.dateofbirth,
        'department': employee.department,
        'gender': employee.gender,
        'status': employee.status,
        'position': employee.position,
        'contact': employee.contact,
        'address': employee.get_address(),
        'age': employee.get_age(),
    }
    return save_api_record('employees', record, 'employee_id')


@app.get('/api/departments')
def list_departments():
    departments = get_records('departments')
    if departments:
        return departments
    return [
        {'department_id': 'dept001', 'name': 'IT', 'staff': []},
        {'department_id': 'dept002', 'name': 'Sales', 'staff': []},
    ]


@app.get('/api/positions')
def list_positions():
    return get_records('positions')


@app.get('/api/payslips')
def list_payslips():
    return get_records('payslips')


@app.post('/api/payroll/calculate')
def calculate_payroll(payload: PayrollCalculation):
    return calculate_pay(payload)


@app.post('/api/payslips', status_code=status.HTTP_201_CREATED)
def create_payslip(payload: PayslipCreate):
    employees = get_records('employees')
    employee = next(
        (
            record
            for record in employees
            if record.get('employee_id') == payload.employee_id
        ),
        None,
    )
    if employee is None:
        raise HTTPException(status_code=404, detail='Employee not found')

    calculation = calculate_pay(payload)
    employee_name = ' '.join(
        value
        for value in (employee.get('first_name'), employee.get('last_name'))
        if value
    )
    record = {
        'payslip_id': payload.payslip_id,
        'payroll_id': payload.payroll_id,
        'employee_id': payload.employee_id,
        'employee_name': employee_name,
        'base_salary': calculation['base_salary'],
        'allowance_rate': calculation['allowance_rate'],
        'allowance_amount': calculation['allowance_amount'],
        'deduction_rate': calculation['deduction_rate'],
        'deduction_amount': calculation['deduction_amount'],
        'hours_worked': calculation['hours_worked'],
        'gross': calculation['gross'],
        'net': calculation['net'],
        'created_at': datetime.now().isoformat(),
    }
    return save_api_record('payslips', record, 'payslip_id')
