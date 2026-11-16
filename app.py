from datetime import date

from flask import Flask, redirect, render_template, request, url_for

from data_store import load_records, save_records
from department import load_departments, save_departments
from main import load_employees, sync_payroll_roster
from oop_prac import (Allowance, Department, Deductions, Employee, Payroll,
                      Payslip, Position, SalaryScale)

app = Flask(__name__)


def get_employees():
    """Load saved employees as Employee objects using the current salaries."""
    scale = get_salary_scale()
    return scale, load_employees(scale)


def get_salary_scale():
    """Fill missing saved positions with the project's default salaries."""
    scale = SalaryScale.defaults()
    scale.update(SalaryScale.load())
    return scale


@app.route("/")
def home():
    return redirect(url_for("departments_page"))


@app.route("/departments")
def departments_page():
    departments = load_departments()
    return render_template("departments.html", departments=departments,
                           error=None, message=request.args.get("message"))


@app.route("/departments/add", methods=["POST"])
def add_department():
    departments = load_departments()
    name = request.form.get("name", "")
    try:
        Department.add_department(departments, name)
        save_departments(departments)
        return redirect(url_for("departments_page", message="Department added."))
    except ValueError as error:
        return render_template("departments.html", departments=departments,
                               error=str(error), message=None)


@app.route("/employees", methods=["GET", "POST"])
def employees():
    error = None
    if request.method == "POST":
        departments = load_departments()
        scale = get_salary_scale()
        department_name = request.form.get("department", "")
        title = request.form.get("position_title", "")
        department = next(
            (item for item in departments
             if item.departmentname == department_name), None
        )

        try:
            if department is None:
                raise ValueError("Choose a valid department.")
            if title not in scale:
                raise ValueError("Choose a valid position.")

            position = Position(title, department.departmentname, scale[title])
            employee = Employee(
                Employee.generate_id(),
                request.form.get("first_name", ""),
                request.form.get("last_name", ""),
                request.form.get("date_of_birth", ""),
                request.form.get("contact", ""),
                request.form.get("village", ""),
                request.form.get("city", ""),
                request.form.get("gender", ""),
                request.form.get("status", "active"),
                position,
                request.form.get("tax_resident") == "yes",
            )
            department.add_staff(employee.to_dict())
            save_departments(departments)
            return redirect(url_for("employees", message="Employee added."))
        except (KeyError, TypeError, ValueError) as problem:
            error = str(problem)

    scale, employee_list = get_employees()
    return render_template(
        "employees.html", employees=employee_list,
        departments=load_departments(), titles=list(scale),
        scale=scale, error=error, message=request.args.get("message")
    )


@app.route("/employees/remove", methods=["POST"])
def remove_employee():
    employee_id = request.form.get("employee_id", "").strip()
    if request.form.get("confirm") != "yes":
        return redirect(url_for("employees", message="Confirm removal first."))

    departments = load_departments()
    found = False
    for department in departments:
        found = department.remove_staff(employee_id) or found
    if not found:
        return redirect(url_for("employees", message="Employee was not found."))
    save_departments(departments)

    saved_allowances = [
        item for item in load_records("allowances")
        if str(item.get("employee_id", "")).casefold() != employee_id.casefold()
    ]
    save_records("allowances", saved_allowances)

    roster = [
        item for item in load_records("payroll_roster")
        if str(item.get("employee_id", "")).casefold() != employee_id.casefold()
    ]
    save_records("payroll_roster", roster)

    updated_payrolls = []
    for payroll in load_records("payrolls"):
        slips = [
            slip for slip in payroll.get("payslips", [])
            if str(slip.get("employee_id", "")).casefold() != employee_id.casefold()
        ]
        if not slips:
            continue
        payroll["payslips"] = slips
        payroll["employee_count"] = len(slips)
        payroll["total_gross"] = sum(slip.get("gross", 0) for slip in slips)
        payroll["total_deductions"] = sum(
            slip.get("total_deductions", 0) for slip in slips
        )
        payroll["total_employer_nssf"] = sum(
            slip.get("employer_nssf", 0) for slip in slips
        )
        payroll["total_net"] = sum(slip.get("net", 0) for slip in slips)
        updated_payrolls.append(payroll)
    save_records("payrolls", updated_payrolls)

    return redirect(url_for("employees", message="Employee and related records removed."))


@app.route("/payroll-roster")
def payroll_roster():
    scale = get_salary_scale()
    roster = sync_payroll_roster(scale)
    return render_template("payroll_roster.html", roster=roster)


@app.route("/positions", methods=["GET", "POST"])
def positions():
    error = None
    if request.method == "POST":
        title = request.form.get("title", "").strip().casefold()
        amount_text = request.form.get("amount", "")
        scale = get_salary_scale()
        try:
            if not title:
                raise ValueError("Position title cannot be empty.")
            if title in scale:
                raise ValueError(f"Position '{title}' already exists.")
            amount = float(amount_text)
            if amount < 0:
                raise ValueError("Salary cannot be negative.")
            scale[title] = amount
            SalaryScale.save(scale)
            return redirect(url_for("positions", message="Position added."))
        except (TypeError, ValueError) as problem:
            error = str(problem)

    return render_template("positions.html", positions=get_salary_scale(),
                           error=error, message=request.args.get("message"))


@app.route("/allowances", methods=["GET", "POST"])
def allowances():
    error = None
    if request.method == "POST":
        employee_id = request.form.get("employee_id", "")
        name = request.form.get("name", "")
        amount_text = request.form.get("amount", "")
        try:
            _, employee_list = get_employees()
            if not any(item.id == employee_id for item in employee_list):
                raise ValueError("Choose a valid employee.")
            allowance = Allowance(
                Allowance.generate_id(), employee_id, name, float(amount_text)
            )
            records = load_records("allowances")
            records.append(allowance.to_dict())
            save_records("allowances", records)
            return redirect(url_for("allowances", message="Allowance added."))
        except (TypeError, ValueError) as problem:
            error = str(problem)

    _, employee_list = get_employees()
    records = load_records("allowances")
    return render_template("allowances.html", allowances=records,
                           employees=employee_list, error=error,
                           message=request.args.get("message"))


@app.route("/salary-scale", methods=["GET", "POST"])
def salary_scale():
    error = None
    if request.method == "POST":
        title = request.form.get("title", "")
        amount_text = request.form.get("amount", "")
        scale = get_salary_scale()
        try:
            if title not in scale:
                raise ValueError("Choose a valid position.")
            amount = float(amount_text)
            if amount < 0:
                raise ValueError("Salary cannot be negative.")
            scale[title] = amount
            SalaryScale.save(scale)
            return redirect(url_for("salary_scale", message="Salary scale updated."))
        except (TypeError, ValueError) as problem:
            error = str(problem)

    return render_template("salary_scale.html", scale=get_salary_scale(),
                           titles=list(get_salary_scale()), error=error,
                           message=request.args.get("message"))


@app.route("/payrolls", methods=["GET", "POST"])
def payrolls():
    error = None
    if request.method == "POST":
        pay_date = request.form.get("pay_date", "").strip() or date.today().isoformat()
        try:
            date.fromisoformat(pay_date)
            scale = get_salary_scale()
            roster = sync_payroll_roster(scale)
            active_ids = {item["employee_id"].casefold() for item in roster}
            employee_list = [
                employee for employee in load_employees(scale)
                if employee.status == "active" and employee.id.casefold() in active_ids
            ]
            if not employee_list:
                raise ValueError("There are no active employees to pay.")

            allowance_items = []
            for record in load_records("allowances"):
                try:
                    allowance_items.append(Allowance.from_dict(record))
                except (KeyError, TypeError, ValueError):
                    continue

            payroll_id = Payroll.generate_id()
            payslips = []
            for employee in employee_list:
                employee_allowances = [
                    item for item in allowance_items
                    if item.employee_id == employee.id
                ]
                allowance_total = sum(item.amount for item in employee_allowances)
                eligible_for_nssf = 16 <= employee.age <= 55
                deductions = Deductions(
                    employee.salary, allowance_total,
                    employee.tax_resident, eligible_for_nssf
                )
                payslips.append(Payslip(
                    employee, payroll_id, pay_date,
                    employee_allowances, deductions
                ))

            payroll = Payroll(payroll_id, pay_date, payslips)
            records = load_records("payrolls")
            records.append(payroll.to_dict())
            save_records("payrolls", records)
            return redirect(url_for("payslips", payroll_id=payroll_id))
        except (TypeError, ValueError) as problem:
            error = str(problem)

    return render_template("payrolls.html", payrolls=load_records("payrolls"),
                           error=error, message=request.args.get("message"))


@app.route("/payslips")
def payslips():
    payroll_id = request.args.get("payroll_id", "")
    employee_id = request.args.get("employee_id", "")
    slips = []
    for payroll in load_records("payrolls"):
        for record in payroll.get("payslips", []):
            if payroll_id and record.get("payroll_id") != payroll_id:
                continue
            if employee_id and record.get("employee_id", "").casefold() != employee_id.casefold():
                continue
            slips.append(Payslip.from_dict(record))
    return render_template("payslips.html", slips=slips,
                           payroll_id=payroll_id, employee_id=employee_id)


if __name__ == "__main__":
    app.run(debug=True)
