"""Command-line entry point for employee and payroll management."""

from datetime import date

from data_store import load_records, save_records
from department import load_departments, save_departments
from oop_prac import (Allowance, Deductions, Department, Employee, Payroll,
                      Payslip, Position, SalaryScale)

ALLOWANCES_FILE = "allowances"
PAYROLL_ROSTER_FILE = "payroll_roster"
PAYROLLS_FILE = "payrolls"


def load_employees(scale):#purpose is to loaf all valid employees firm the departments and turn their saved json into their saved json records
    result = []
    for department in load_departments():
        for record in department.staff:
            if not isinstance(record, dict):
                continue
            title = record.get("position_title", "regular worker")
            if not isinstance(title, str):
                continue
            if title not in Position.TITLES or title not in scale:
                continue
            position = Position(title, department.departmentname, scale[title])
            try:
                result.append(Employee.from_dict(record, position))
            except (TypeError, ValueError):
                print(f"Skipping invalid employee record: {record.get('id', '?')}")
    return result


def sync_payroll_roster(scale):
    """Keep the payroll roster in sync with active employees."""
    roster = []
    for employee in load_employees(scale):
        if employee.status == "active":
            roster.append({
                "employee_id": employee.id,
                "employee_name": employee.full_name,
                "position": employee.position.title,
                "department": employee.department,
                "monthly_salary": employee.salary,
            })
    save_records(PAYROLL_ROSTER_FILE, roster)
    return roster


def show_payroll_roster(scale):
    roster = sync_payroll_roster(scale)
    if not roster:
        print("No active employees are in the payroll roster.")
        return
    print("\nActive payroll roster:")
    for employee in roster:
        print(f"{employee['employee_id']} | {employee['employee_name']} | "
              f"{employee['position']} | {employee['department']} | "
              f"UGX {employee['monthly_salary']:,.2f}")


def select_department(departments):
    if not departments:
        print("There are no departments yet.")
        return None
    print("\nDepartments:")
    for index, department in enumerate(departments, start=1):
        print(f"{index}. {department.departmentname}")
    choice = input("Choose a department number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(departments):
        print("Invalid department selection.")
        return None
    return departments[int(choice) - 1]


def add_department(departments):
    name = input("New department name: ").strip()
    try:
        department = Department.add_department(departments, name)
    except ValueError as error:
        print(error)
        return
    save_departments(departments)
    print(f"Added {department.departmentname}.")


def add_employee(departments, scale):
    employee_id = Employee.generate_id()
    print(f"Generated employee ID: {employee_id}")
    title_choices = Position.TITLES
    print("Positions:")
    for index, title in enumerate(title_choices, start=1):
        print(f"{index}. {title} - UGX {scale[title]:,.2f}")
    title_choice = input("Choose a position number: ").strip()
    if not title_choice.isdigit() or not 1 <= int(title_choice) <= len(title_choices):
        print("Invalid position selection.")
        return
    department = select_department(departments)
    if department is None:
        return
    title = title_choices[int(title_choice) - 1]
    position = Position(title, department.departmentname, scale[title])
    try:
        tax_resident_input = input("Tax resident in Uganda? (y/n, default y): ").strip().casefold()
        tax_resident = tax_resident_input not in {"n", "no"}
        employee = Employee(
            employee_id,
            input("First name: "), input("Last name: "),
            input("Date of birth (YYYY-MM-DD): ").strip(),
            input("Contact: ").strip(), input("Village: ").strip(), input("City: ").strip(),
            input("Gender: ").strip(),
            input("Status (active/inactive, default active): ").strip() or "active",
            position,
            tax_resident,
        )
    except ValueError as error:
        print(f"Could not add employee: {error}")
        return
    department.add_staff(employee.to_dict())
    save_departments(departments)
    print(f"Added {employee.full_name}; salary scale: UGX {employee.salary:,.2f} per month.")
    if employee.status == "active":
        sync_payroll_roster(scale)
        print("Added to the active payroll roster.")


def show_employees(scale):
    employees = load_employees(scale)
    if not employees:
        print("No employees have been added yet.")
        return
    for employee in employees:
        print(f"{employee.id} | {employee.full_name} | {employee.position.title} | "
              f"{employee.department} | {employee.status.title()} | "
              f"UGX {employee.salary:,.2f} | Age {employee.age}")


def add_allowance(scale):
    employees = load_employees(scale)
    employee_id = input("Employee ID for this allowance: ").strip()
    employee_found = False
    for employee in employees:
        if employee.id.casefold() == employee_id.casefold():
            employee_found = True
            break
    if not employee_found:
        print("Employee not found.")
        return
    name = input("Allowance name: ").strip()
    try:
        amount = float(input("Monthly allowance amount (UGX): ").strip())
        allowance = Allowance(Allowance.generate_id(), employee_id, name, amount)
    except ValueError as error:
        print(f"Invalid allowance: {error}")
        return
    records = load_records(ALLOWANCES_FILE)
    records.append(allowance.to_dict())
    save_records(ALLOWANCES_FILE, records)
    print(f"Added {name} allowance for {employee_id}.")


def remove_employee(scale):
    employees = load_employees(scale)
    if not employees:
        print("There are no employees to remove.")
        return

    print("\nEmployees:")
    for employee in employees:
        print(f"{employee.id} | {employee.full_name} | {employee.department}")
    employee_id = input("Employee ID to remove: ").strip().casefold()

    selected = None
    for employee in employees:
        if employee.id.casefold() == employee_id:
            selected = employee
            break
    if selected is None:
        print("Employee not found.")
        return

    confirmation = input(
        f"Remove {selected.full_name}, their allowances, roster entry, and saved payslips? (y/n): "
    ).strip().casefold()
    if confirmation not in {"y", "yes"}:
        print("Removal cancelled.")
        return

    # Remove the employee from the department staff list.
    departments = load_departments()
    for department in departments:
        department.remove_staff(selected.id)
    save_departments(departments)

    # Remove allowances assigned to this employee.
    allowances = []
    for item in load_records(ALLOWANCES_FILE):
        if str(item.get("employee_id", "")).casefold() != selected.id.casefold():
            allowances.append(item)
    save_records(ALLOWANCES_FILE, allowances)

    # Remove their roster entry.
    roster = []
    for item in load_records(PAYROLL_ROSTER_FILE):
        if str(item.get("employee_id", "")).casefold() != selected.id.casefold():
            roster.append(item)
    save_records(PAYROLL_ROSTER_FILE, roster)

    # Remove their payslips and recalculate totals for each affected payroll.
    updated_payrolls = []
    for payroll in load_records(PAYROLLS_FILE):
        remaining_slips = []
        for slip in payroll.get("payslips", []):
            if str(slip.get("employee_id", "")).casefold() != selected.id.casefold():
                remaining_slips.append(slip)
        if not remaining_slips:
            continue

        payroll["payslips"] = remaining_slips
        payroll["employee_count"] = len(remaining_slips)
        payroll["total_gross"] = sum(slip.get("gross", 0) for slip in remaining_slips)
        payroll["total_deductions"] = sum(
            slip.get("total_deductions", 0) for slip in remaining_slips)
        payroll["total_employer_nssf"] = sum(
            slip.get("employer_nssf", 0) for slip in remaining_slips)
        payroll["total_net"] = sum(slip.get("net", 0) for slip in remaining_slips)
        updated_payrolls.append(payroll)
    save_records(PAYROLLS_FILE, updated_payrolls)

    sync_payroll_roster(scale)
    print(f"Removed {selected.full_name} and their connected payroll records.")


def edit_salary_scale(scale):
    print("\nMonthly salary scale (UGX):")
    for index, title in enumerate(Position.TITLES, start=1):
        print(f"{index}. {title}: {scale[title]:,.2f}")
    choice = input("Choose a position to edit (Enter to cancel): ").strip()
    if not choice:
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(Position.TITLES):
        print("Invalid position selection.")
        return
    title = Position.TITLES[int(choice) - 1]
    try:
        amount = float(input(f"New monthly salary for {title} (UGX): ").strip())
        if amount < 0:
            raise ValueError("Salary cannot be negative.")
    except ValueError as error:
        print(f"Invalid salary: {error}")
        return
    scale[title] = amount
    SalaryScale.save(scale)
    print("Salary scale updated. New values apply to future payroll runs.")


def run_payroll(scale):
    roster = sync_payroll_roster(scale)
    roster_ids = []
    for item in roster:
        roster_ids.append(str(item["employee_id"]).casefold())
    employees = []
    for employee in load_employees(scale):
        if employee.status == "active" and employee.id.casefold() in roster_ids:
            employees.append(employee)
    if not employees:
        print("There are no active employees to pay.")
        return
    pay_date = input(f"Payroll date (YYYY-MM-DD, default {date.today().isoformat()}): ").strip()
    if not pay_date:
        pay_date = date.today().isoformat()
    try:
        date.fromisoformat(pay_date)
    except ValueError:
        print("Enter a valid date in YYYY-MM-DD format.")
        return
    records = load_records(PAYROLLS_FILE)
    payroll_id = Payroll.generate_id()
    allowances = []
    for row in load_records(ALLOWANCES_FILE):
        if isinstance(row, dict):
            allowances.append(Allowance.from_dict(row))
    payslips = []
    for employee in employees:
        employee_allowances = []
        for item in allowances:
            if item.employee_id == employee.id:
                employee_allowances.append(item)
        total_allowances = sum(item.amount for item in employee_allowances)
        nssf_eligible = 16 <= employee.age <= 55
        deduction = Deductions(employee.salary, total_allowances,
                               employee.tax_resident, nssf_eligible)
        payslips.append(Payslip(employee, payroll_id, pay_date, employee_allowances, deduction))
    payroll = Payroll(payroll_id, pay_date, payslips)
    records.append(payroll.to_dict())
    save_records(PAYROLLS_FILE, records)
    print(f"\nPayroll {payroll.payrollid} - {payroll.date}")
    print(f"Employees paid:    {len(payslips)}")
    print(f"Total gross pay:   UGX {payroll.total_gross:,.2f}")
    print(f"Total deductions:  UGX {payroll.total_deductions:,.2f}")
    print(f"Employer NSSF:     UGX {payroll.total_employer_nssf:,.2f}")
    print(f"Total net pay:     UGX {payroll.total_net:,.2f}")


def show_payslip():
    records = load_records(PAYROLLS_FILE)
    payroll_id = input("Payroll ID: ").strip()
    employee_id = input("Employee ID: ").strip()
    for record in records:
        if record.get("id") == payroll_id:
            for item in record.get("payslips", []):
                if str(item.get("employee_id", "")).casefold() == employee_id.casefold():
                    Payslip.from_dict(item).display()
                    return
            print("That employee has no payslip in this payroll run.")
            return
    print("Payroll run not found.")


def main():
    departments = load_departments()
    save_departments(departments)
    scale = SalaryScale.load()
    for title in Position.TITLES:
        scale.setdefault(title, SalaryScale.defaults()[title])
    SalaryScale.save(scale)
    sync_payroll_roster(scale)
    while True:
        print("\n=== EMPLOYEE PAYROLL SYSTEM ===")
        print("1. List departments")
        print("2. Add department")
        print("3. Add employee")
        print("4. List employees")
        print("5. View active payroll roster")
        print("6. Remove employee")
        print("7. Add employee allowance")
        print("8. View or update salary scale")
        print("9. Run payroll")
        print("10. View payslip")
        print("11. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            for department in departments:
                print(f"{department.deptid} | {department.departmentname}")
        elif choice == "2":
            add_department(departments)
        elif choice == "3":
            add_employee(departments, scale)
        elif choice == "4":
            show_employees(scale)
        elif choice == "5":
            show_payroll_roster(scale)
        elif choice == "6":
            remove_employee(scale)
        elif choice == "7":
            add_allowance(scale)
        elif choice == "8":
            edit_salary_scale(scale)
        elif choice == "9":
            run_payroll(scale)
        elif choice == "10":
            show_payslip()
        elif choice == "11":
            print("Goodbye.")
            break
        else:
            print("Choose a number from 1 to 11.")


if __name__ == "__main__":
    main()
