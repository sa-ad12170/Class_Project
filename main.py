import json

from oop_prac import Allowance, Deduction, Department, Employee, Payroll, Payslip, Salary


DATA_FILE = "main.json"

# Keep all saved records under these three top-level keys.
try:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

if not isinstance(data, dict):
    data = {}

data.setdefault("departments", [])
data.setdefault("allowances", [])
data.setdefault("payrolls", [])


# Collect employee and department details.
first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
birth_year = int(input("Enter birth year: "))
department_name = input("Enter department: ")
gender = input("Enter gender: ")
status = input("Enter status: ")
contact = input("Enter contact: ")
position = input("Enter position: ")
village = input("Enter village: ")
city = input("Enter city: ")

employee = Employee(
    first_name,
    last_name,
    birth_year,
    department_name,
    gender,
    status,
    contact,
    village,
    city,
    position,
)

employee_record = {
    "id": employee.empid,
    "first_name": employee.firstname,
    "last_name": employee.lastname,
    "birth_year": employee.dateofbirth,
    "gender": employee.gender,
    "status": employee.status,
    "position": employee.position,
    "contact": employee.contact,
    "address": employee.get_address(),
    "age": employee.get_age(),
}

# Find this department by name, or create it with an empty staff list.
department = None
for saved_department in data["departments"]:
    if saved_department["name"].lower() == department_name.lower():
        department = saved_department
        break

if department is None:
    department = {
        "id": Department.generate_id(),
        "name": department_name,
        "staff": [],
    }
    data["departments"].append(department)

department["staff"].append(employee_record)


# Collect salary details and create one payroll record.
hours_worked = int(input("Enter hours worked: "))
rate_per_hour = int(input("Enter rate per hour: "))
salary = Salary(employee.empid, employee.firstname, hours_worked, rate_per_hour)

payroll = Payroll()
allowance_records = []
allowance_amounts = []

while True:
    allowance_name = input("Enter allowance name (Housing, Transport, Medical, Internet): ")
    allowance = Allowance(payroll.payrollid, employee.empid, allowance_name)
    allowance_amount = allowance.fixed_allowance()

    if not isinstance(allowance_amount, (int, float)):
        print("Unknown allowance name. Please choose one of the listed names.")
        continue

    allowance_record = {
        "id": allowance.id,
        "payroll_id": allowance.payrollid,
        "employee_id": allowance.employmentid,
        "name": allowance.name,
        "amount": allowance_amount,
    }
    data["allowances"].append(allowance_record)
    allowance_records.append(allowance_record)
    allowance_amounts.append(allowance_amount)

    if input("Add another allowance? (y/n): ").lower() != "y":
        break

total_allowances = sum(allowance_amounts)

deduction_records = []
deduction_amounts = []
while True:
    deduction_name = input("Enter deduction name (NSSF, PAYE, Fine): ")
    deduction = Deduction(deduction_name, payroll.payrollid, employee.empid)
    deduction_amount = deduction.fixed_deductions()

    if not isinstance(deduction_amount, (int, float)):
        print("Unknown deduction name. Please choose one of the listed names.")
        continue

    deduction_records.append(
        {
            "id": deduction.id,
            "name": deduction.deduction_name,
            "amount": deduction_amount,
        }
    )
    deduction_amounts.append(deduction_amount)

    if input("Add another deduction? (y/n): ").lower() != "y":
        break

total_deductions = sum(deduction_amounts)
payslip = Payslip(
    employee.firstname,
    total_deductions,
    total_allowances,
    salary.hoursworked,
)
payslip.set_gross(salary.salaryamount)
payslip.compute_net()

data["payrolls"].append(
    {
        "id": payroll.payrollid,
        "date": payroll.date.isoformat(),
        "employee_id": employee.empid,
        "salary": {
            "hours_worked": salary.hoursworked,
            "rate_per_hour": salary.rateperhour,
            "amount": salary.get_salary(),
        },
        "deductions": deduction_records,
        "payslip": {
            "id": payslip.id,
            "total_allowances": total_allowances,
            "total_deductions": total_deductions,
            "gross": payslip.get_gross(),
            "net": payslip.get_net(),
        },
    }
)

with open(DATA_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Employee and payroll data saved to main.json")
