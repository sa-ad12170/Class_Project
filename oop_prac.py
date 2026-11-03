"""Core payroll classes for the project.

All model classes live here by design. The small module files in the project
re-export these classes to keep older imports working.
"""

from abc import ABC, abstractmethod
from datetime import date
from data_store import load_records, save_records

class Department:
    def __init__(self, deptid, name):
        self.deptid = str(deptid)
        self.departmentname = str(name).strip()
        self.staff = []

    @classmethod
    def add_department(cls, departments, name):
        name = str(name).strip()
        if not name:
            raise ValueError("Department name cannot be empty.")
        for item in departments:
            if item.departmentname.casefold() == name.casefold():
                raise ValueError(f"Department '{name}' already exists.")
        department = cls(f"dept{len(departments) + 1:03d}", name)
        departments.append(department)
        return department

    def add_staff(self, employee):
        for member in self.staff:
            if member.get("id") == employee.get("id"):
                return self.staff
        self.staff.append(employee)
        return self.staff

    def remove_staff(self, employee_id):
        for employee in self.staff:
            if employee.get("id") == employee_id:
                self.staff.remove(employee)
                return True
        return False

    def get_no_of_staff(self):
        return len(self.staff)

    def to_dict(self):
        return {"id": self.deptid, "name": self.departmentname, "staff": self.staff}

    @classmethod
    def from_dict(cls, record):
        department = cls(record["id"], record["name"])
        department.staff = record.get("staff", [])
        return department


class SalaryScale:
    DEFAULTS = {
        "regular worker": 500_000,
        "team lead": 7_000_000,
        "department head": 900_000,
        "ceo": 2_000_000,
        "coo": 40_000_000,
    }
    DATA_SECTION = "salary_scales"

    def __init__(self, title, amount):
        self.title = str(title)
        if self.title not in self.DEFAULTS:
            raise ValueError(f"Unknown position title: {title}")
        self.amount = float(amount)
        if self.amount < 0:
            raise ValueError("Salary cannot be negative.")

    def to_dict(self):
        return {"title": self.title, "amount": self.amount}

    @classmethod
    def defaults(cls):
        scale = {}
        for title, amount in cls.DEFAULTS.items():
            scale[title] = float(amount)
        return scale

    @classmethod
    def load(cls):
        # Class methods work with the shared salary scale, so no SalaryScale
        # object needs to be created just to load or save it.
        records = load_records(cls.DATA_SECTION)
        if not records:
            scale = cls.defaults()
            cls.save(scale)
            return scale
        scale = {}
        for row in records:
            if isinstance(row, dict) and "title" in row and "amount" in row:
                title = str(row["title"])
                if title in cls.DEFAULTS:
                    scale[title] = float(row["amount"])
        return scale

    @classmethod
    def save(cls, scale):
        records = []
        for title, amount in scale.items():
            records.append(cls(title, amount).to_dict())
        save_records(cls.DATA_SECTION, records)

    @classmethod
    def get_salary(cls, title, scale=None):
        scale = cls.load() if scale is None else scale
        key = str(title)
        if key not in cls.DEFAULTS or key not in scale:
            raise KeyError(f"No salary scale is defined for '{title}'.")
        return float(scale[key])


class Position:
    TITLES = ("regular worker", "department head", "team lead", "ceo", "coo")

    def __init__(self, title, department, salary=None):
        self.title = str(title)
        if self.title not in self.TITLES:
            raise ValueError(f"Unknown position title: {title}")
        self.department = str(department).strip()
        self.salary = SalaryScale.get_salary(self.title) if salary is None else float(salary)

    def to_dict(self):
        return {"title": self.title, "department": self.department,
                "salary": self.salary}

    def __str__(self):
        return f"{self.title} - {self.department} (UGX {self.salary:,.2f})"


class Employee:
    def __init__(self, employee_id, firstname, lastname, dateofbirth, contact,
                 village, city, gender, status, position, tax_resident=True):
        self.id = str(employee_id).strip()
        self.firstname = str(firstname).strip()
        self.lastname = str(lastname).strip()
        self.dateofbirth = date.fromisoformat(str(dateofbirth))
        self.contact = str(contact).strip()
        self.village = str(village).strip()
        self.city = str(city).strip()
        self.gender = str(gender).strip()
        self.status = str(status).strip().casefold()
        self.position = position
        self.tax_resident = bool(tax_resident)
        if not self.id or not self.firstname or not self.lastname:
            raise ValueError("Employee ID and full name are required.")
        if not self.status:
            raise ValueError("Employee status is required.")

    @classmethod
    def generate_id(cls):
        """Return the next unused employee ID, such as Emp001 or Emp002."""
        highest_number = 0
        departments = load_records("departments")
        for department in departments:
            if not isinstance(department, dict):
                continue
            for employee in department.get("staff", []):
                if not isinstance(employee, dict):
                    continue
                employee_id = str(employee.get("id", ""))
                if employee_id.startswith("Emp") and employee_id[3:].isdigit():
                    number = int(employee_id[3:])
                    if number > highest_number:
                        highest_number = number
        return f"Emp{highest_number + 1:03d}"

    # These properties calculate values from existing fields, avoiding stored duplicates.
    @property
    def age(self):
        today = date.today()
        age = today.year - self.dateofbirth.year
        birthday_has_passed = (today.month, today.day) >= (
            self.dateofbirth.month, self.dateofbirth.day)
        if not birthday_has_passed:
            age -= 1
        return age

    @property
    def department(self):
        return self.position.department

    @property
    def salary(self):
        return self.position.salary

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def address(self):
        parts = []
        if self.village:
            parts.append(self.village)
        if self.city:
            parts.append(self.city)
        return ", ".join(parts)

    def get_age(self):
        return self.age

    def get_address(self):
        return self.address

    def compute_salary(self):
        return self.salary

    def to_dict(self):
        return {
            "id": self.id, "first_name": self.firstname, "last_name": self.lastname,
            "date_of_birth": self.dateofbirth.isoformat(), "contact": self.contact,
            "village": self.village, "city": self.city, "gender": self.gender,
            "status": self.status, "position_title": self.position.title,
            "department": self.department, "tax_resident": self.tax_resident,
        }

    @classmethod
    def from_dict(cls, record, position):
        """Build an Employee object from one JSON record."""
        return cls(record["id"], record["first_name"], record["last_name"],
                   record["date_of_birth"], record.get("contact", ""),
                   record.get("village", ""), record.get("city", ""),
                   record.get("gender", ""), record.get("status", "active"), position,
                   record.get("tax_resident", True))


class Deductions:
    """Uganda monthly NSSF and PAYE calculations, using FY 2026/27 PAYE rates."""

    EMPLOYEE_NSSF_RATE = 0.05
    EMPLOYER_NSSF_RATE = 0.10
    HIGH_INCOME_THRESHOLD = 10_000_000.0

    def __init__(self, salary, allowances=0.0, resident=True, nssf_eligible=True):
        self.salary = float(salary)
        self.allowances = float(allowances)
        self.gross = max(0.0, self.salary + self.allowances)
        # Uganda's employee NSSF contribution is not deducted before PAYE.
        self.nssf = self.compute_nssf(self.gross) if nssf_eligible else 0.0
        self.employer_nssf = self.compute_employer_nssf(self.gross) if nssf_eligible else 0.0
        self.paye = self.compute_paye(self.gross, resident=resident)
        self.total = round(self.nssf + self.paye, 2)

    def compute_nssf(self, gross_pay):
        return round(max(0.0, float(gross_pay)) * self.EMPLOYEE_NSSF_RATE, 2)

    def compute_employer_nssf(self, gross_pay):
        return round(max(0.0, float(gross_pay)) * self.EMPLOYER_NSSF_RATE, 2)

    def compute_paye(self, chargeable_income, resident=True):
        """Apply the progressive monthly PAYE bands for the employee's tax status."""
        income = max(0.0, float(chargeable_income))
        if resident:
            if income <= 335_000:
                tax = 0.0
            elif income <= 410_000:
                tax = 0.20 * (income - 335_000)
            elif income <= 485_000:
                tax = 15_000 + 0.25 * (income - 410_000)
            elif income <= self.HIGH_INCOME_THRESHOLD:
                tax = 33_750 + 0.30 * (income - 485_000)
            else:
                tax = (33_750 + 0.30 * (income - 485_000)
                       + 0.10 * (income - self.HIGH_INCOME_THRESHOLD))
        else:
            if income <= 335_000:
                tax = 0.10 * income
            elif income <= 410_000:
                tax = 33_500 + 0.20 * (income - 335_000)
            elif income <= self.HIGH_INCOME_THRESHOLD:
                tax = 48_500 + 0.30 * (income - 410_000)
            else:
                tax = (48_500 + 0.30 * (income - 410_000)
                       + 0.10 * (income - self.HIGH_INCOME_THRESHOLD))
        return round(max(0.0, tax), 2)

    def to_dict(self):
        return {"gross": round(self.gross, 2), "nssf": self.nssf,
                "employer_nssf": self.employer_nssf,
                "paye": self.paye, "total": self.total}


class Allowance:
    def __init__(self, allowance_id, employee_id, name, amount):
        self.id = str(allowance_id)
        self.employee_id = str(employee_id)
        self.name = str(name).strip()
        self.amount = float(amount)
        if not self.name:
            raise ValueError("Allowance name is required.")
        if self.amount < 0:
            raise ValueError("Allowance cannot be negative.")

    @classmethod
    def generate_id(cls):
        """Make an allowance ID from today's date and the saved allowance count."""
        allowance_count = len(load_records("allowances")) + 1
        return f"ALW-{date.today():%Y%m%d}-{allowance_count:03d}"

    def to_dict(self):
        return {"id": self.id, "employee_id": self.employee_id,
                "name": self.name, "amount": self.amount}

    @classmethod
    def from_dict(cls, record):
        return cls(record["id"], record["employee_id"], record["name"], record["amount"])


class Payroll:
    def __init__(self, payroll_id, pay_date=None, payslips=None):
        self.payrollid = str(payroll_id)
        self.date = pay_date or date.today().isoformat()
        self.payslips = payslips or []

    @classmethod
    def generate_id(cls):
        """Make the next sequential payroll ID, such as PR001 or PR002."""
        payrolls = load_records("payrolls")
        highest_number = 0
        for payroll in payrolls:
            payroll_id = str(payroll.get("id", ""))
            if payroll_id.startswith("PR") and payroll_id[2:].isdigit():
                number = int(payroll_id[2:])
                if number > highest_number:
                    highest_number = number
        next_number = max(highest_number, len(payrolls)) + 1
        return f"PR{next_number:03d}"

    @property
    def total_gross(self):
        total = 0
        for slip in self.payslips:
            total += slip.gross
        return round(total, 2)

    @property
    def total_deductions(self):
        total = 0
        for slip in self.payslips:
            total += slip.total_deductions
        return round(total, 2)

    @property
    def total_employer_nssf(self):
        total = 0
        for slip in self.payslips:
            total += slip.employer_nssf
        return round(total, 2)

    @property
    def total_net(self):
        total = 0
        for slip in self.payslips:
            total += slip.net
        return round(total, 2)

    def to_dict(self):
        saved_payslips = []
        for payslip in self.payslips:
            saved_payslips.append(payslip.to_dict())
        return {"id": self.payrollid, "date": self.date,
                "employee_count": len(self.payslips),
                "total_gross": self.total_gross,
                "total_deductions": self.total_deductions,
                "total_employer_nssf": self.total_employer_nssf,
                "total_net": self.total_net,
                "payslips": saved_payslips}

    @classmethod
    def from_dict(cls, record):
        slips = [Payslip.from_dict(item) for item in record.get("payslips", [])]
        return cls(record["id"], record["date"], slips)


class Pay(ABC):
    """Abstract parent: each payment type must provide its own Payments()."""

    @abstractmethod
    def Payments(self):
        pass


class Payslip(Pay):
    """A saved payroll result. It implements the payment display required by Pay."""
    def __init__(self, employee, payroll_id, pay_date, allowance_items, deductions):
        self.employee_id = employee.id
        self.employee_name = employee.full_name
        self.position = employee.position.title
        self.department = employee.department
        self.payroll_id = payroll_id
        self.pay_date = pay_date
        self.basic_salary = round(employee.salary, 2)
        self.allowances = []
        for item in allowance_items:
            self.allowances.append({"name": item.name, "amount": round(item.amount, 2)})
        self.total_allowances = 0
        for item in self.allowances:
            self.total_allowances += item["amount"]
        self.total_allowances = round(self.total_allowances, 2)
        self.gross = round(self.basic_salary + self.total_allowances, 2)
        self.nssf = deductions.nssf
        self.employer_nssf = deductions.employer_nssf
        self.paye = deductions.paye
        self.total_deductions = round(self.nssf + self.paye, 2)
        self.net = round(self.gross - self.total_deductions, 2)

    def to_dict(self):
        return {"employee_id": self.employee_id, "employee_name": self.employee_name,
                "position": self.position, "department": self.department,
                "payroll_id": self.payroll_id, "pay_date": self.pay_date,
                "basic_salary": self.basic_salary, "allowances": self.allowances,
                "total_allowances": self.total_allowances, "gross": self.gross,
                "nssf": self.nssf, "employer_nssf": self.employer_nssf,
                "paye": self.paye, "total_deductions": self.total_deductions,
                "net": self.net}

    @classmethod
    def from_dict(cls, record):
        # A saved payslip is a historical snapshot. Rebuild its saved values
        # directly instead of recalculating them from today's salary scale.
        slip = cls.__new__(cls)
        slip.employee_id = record.get("employee_id", "")
        slip.employee_name = record.get("employee_name", "")
        slip.position = record.get("position", "")
        slip.department = record.get("department", "")
        slip.payroll_id = record.get("payroll_id", "")
        slip.pay_date = record.get("pay_date", "")
        slip.basic_salary = record.get("basic_salary", 0.0)
        slip.allowances = record.get("allowances", [])
        slip.total_allowances = record.get("total_allowances", 0.0)
        slip.gross = record.get("gross", 0.0)
        slip.nssf = record.get("nssf", 0.0)
        slip.employer_nssf = record.get("employer_nssf", 0.0)
        slip.paye = record.get("paye", 0.0)
        slip.total_deductions = record.get("total_deductions", 0.0)
        slip.net = record.get("net", 0.0)
        return slip

    def display(self):
        print(f"\nPAYSLIP - {self.payroll_id} - {self.pay_date}")
        print(f"Employee: {self.employee_name} ({self.employee_id})")
        print(f"Position: {self.position} | Department: {self.department}")
        print(f"Basic salary:       UGX {self.basic_salary:,.2f}")
        for item in self.allowances:
            print(f"{item['name']}:".ljust(20) + f"UGX {item['amount']:,.2f}")
        print(f"Gross pay:          UGX {self.gross:,.2f}")
        print(f"NSSF employee 5%:   UGX {self.nssf:,.2f}")
        print(f"PAYE:               UGX {self.paye:,.2f}")
        print(f"Employee deductions:UGX {self.total_deductions:,.2f}")
        print(f"NSSF employer 10%:  UGX {self.employer_nssf:,.2f}")
        print(f"NET PAY:            UGX {self.net:,.2f}")

    def Payments(self):
        self.display()
