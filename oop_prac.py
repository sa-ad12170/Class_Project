from abc import ABC , abstractmethod


def _non_negative_number(value, field_name):
    """Return a numeric value and reject invalid or negative input."""
    if isinstance(value, bool):
        raise ValueError(f'{field_name} must be a number')

    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f'{field_name} must be a number') from error

    if number < 0:
        raise ValueError(f'{field_name} cannot be negative')

    return int(number) if number.is_integer() else number


def _percentage(value, field_name):
    percentage = _non_negative_number(value, field_name)
    if percentage > 100:
        raise ValueError(f'{field_name} cannot exceed 100')
    return percentage


class Department:
    def __init__(self,deptid,name):
       self.deptid = deptid
       self.departmentname =name
       self.staff = []

    def add_staff(self,employee):
        employee_id = employee.get('employee_id', employee.get('id'))
        if not employee_id:
            raise ValueError('Employee ID is required')
        if any(
            saved.get('employee_id', saved.get('id')) == employee_id
            for saved in self.staff
        ):
            raise ValueError(f'Employee {employee_id} is already in this department')
        self.staff.append (employee)
        return self.staff

    def remove_staff(self,employee_id):
        for employee in self.staff:
            saved_id = employee.get('employee_id', employee.get('id'))
            if saved_id == employee_id:
                self.staff.remove(employee)
                return 'Staff member has been removed'
        return 'Staff member not found'

    def display_staff(self):
        print (f'Staff in {self.departmentname}:')
        if len(self.staff) == 0 :
            print ('No staff in this department ')
        for employee in self.staff :
            employee_id = employee.get('employee_id', employee.get('id'))
            print(f"ID : {employee_id}\nName : {employee['name']}\nPosition:{employee['position']}")

    def get_no_of_staff(self)  :
        return len(self.staff) 
    #converting the class into  a json 
    def to_dict (self )    :
        return {
            'department_id': self.deptid,
            'name': self.departmentname,
            'staff': self.staff,
        }


class Position:
    def __init__(self, title, department, salary, employee=None):
        self.title = str(title).strip()
        if not self.title:
            raise ValueError('Position title is required')

        self.department = department
        self.salary = _non_negative_number(salary, 'Position salary')
        self.employee = employee

    def __str__(self):
        return (
            f'Title: {self.title}\n'
            f'Department: {self.department}\n'
            f'Salary: {self.salary}\n'
            f'Status: {self.status()}'
        )

    def status(self):
        return 'Occupied' if self.employee is not None else 'Vacant'

    def assign_employee(self, employee):
        if self.employee is not None:
            raise ValueError('Position is already occupied')
        self.employee = employee
        return self.status()

    def remove_employee(self):
        employee = self.employee
        self.employee = None
        return employee
    

   



class Employee:
    employee = 0



    def __init__(self,id,firstname,lastname,dateofbirth,department,gender,status,contact,village,city,position):
        self.id =id
        self.firstname =firstname
        self.lastname =lastname
        self.dateofbirth =dateofbirth
        self.department =department#composition
        self.contact = contact
        self.village = village 
        self.city = city
        self.__address = self.set_address()#irrelevant
        self.gender =gender
        self.status =status#fired or active
        position_name = position.title if isinstance(position, Position) else position
        if not str(position_name).strip():
            raise ValueError('Employee position is required')
        self.position = str(position_name).strip().upper()
        self.__age = self.compute_age()
        self._salary = 0
    @classmethod
    def generate_id(cls):
        al = "Emp"
        cls.employee +=1 
        return al + str(cls.employee) 

    



    def set_address (self):
        self.__address = f'{self.village.upper()} in {self.city.upper()}'
        return self.__address
    
    def get_address (self):
        return self.__address

#automatically used to compute age 
    def compute_age(self):
        from datetime import datetime
        currentyear = datetime.today().year
        self.__age = currentyear - int(self.dateofbirth)
        return self.__age 
    def get_age (self):
        return self.__age
    def compute_salary(self):
        return self._salary

    def get_salary(self):
        return self._salary
    
# Inheritance and polymorphism examples.
class Developer(Employee):

    SALARY = 500000
    BONUS1 = 100000
    BONUS2 = 200000
    BONUS3 = 300000
    def __init__(self, id, firstname, lastname, dateofbirth, department, gender, status, contact, village, city, position,language , projects , ):
        super().__init__(id, firstname, lastname, dateofbirth, department, gender, status, contact, village, city, position) 
        self.language = language
        self.projects = int(_non_negative_number(projects, 'Projects'))
        self.compute_salary()

    def compute_salary(self):
        if self.projects < 5:
            self._salary = self.SALARY + self.BONUS1
        elif self.projects <= 10:
            self._salary = self.SALARY + self.BONUS2
        else:
            self._salary = self.SALARY + self.BONUS3
        return self._salary

class Technician(Employee):
    SALARY = 300000
    BONUS1 = 50000
    BONUS2 =100000
    BONUS3 = 150000
    def __init__(self, id, firstname, lastname, dateofbirth, department, gender, status, contact, village, city, position,skills ,tasks ):
        super().__init__(id, firstname, lastname, dateofbirth, department, gender, status, contact, village, city, position)
        self.skills = skills
        self.tasks = int(_non_negative_number(tasks, 'Tasks'))
        self.compute_salary()

    def compute_salary(self):
        if self.tasks < 5:
            self._salary = self.SALARY + self.BONUS1
        elif self.tasks <= 10:
            self._salary = self.SALARY + self.BONUS2
        else:
            self._salary = self.SALARY + self.BONUS3
        return self._salary



class Admin (Employee):
    CEO_SALARY = 100000
    COO_SALARY = 20000000000
    DEFAULT_SALARY = 3000000

    def __init__(self, id, firstname, lastname, dateofbirth, department, gender, status, contact, village, city, position,no_of_people):
        super().__init__(id, firstname, lastname, dateofbirth, department, gender, status, contact, village, city, position)
        self.people = int(_non_negative_number(no_of_people, 'Number of people'))
        self.compute_salary()

    def compute_salary(self):
        if self.position == 'CEO':
            self._salary = self.CEO_SALARY
        elif self.position == 'COO':
            self._salary = self.COO_SALARY
        else:
            self._salary = self.DEFAULT_SALARY
        return self._salary







class Salary:
    """Calculate an employee's salary from hours worked and hourly rate."""

    def __init__(self, employee_id, hoursworked, rateperhour):
        self.employee_id = employee_id
        self.hoursworked = _non_negative_number(hoursworked, 'Hours worked')
        self.rateperhour = _non_negative_number(rateperhour, 'Rate per hour')
        self.__salary = self.compute_salary()

    def compute_salary(self):
        self.__salary = self.hoursworked * self.rateperhour
        return self.__salary

    def get_salary(self):
        return self.__salary


class SalaryScale:
    SALARIES = {
        'regular': 500000,
        'team_leader': 7000000,
        'department_head': 900000,
        'ceo': 2000000,
        'coo': 40000000,
    }

    def __init__(self, employeeid, position):
        self.employeeid = employeeid
        self.position = str(position).strip().lower().replace(' ', '_')
        if self.position not in self.SALARIES:
            available = ', '.join(self.SALARIES)
            raise ValueError(f'Position must be one of: {available}')
        self.salary = self.SALARIES[self.position]

    def get_salary(self):
        return self.salary


class Deductions:
    def __init__(self,id,deductionname,deductionrate,payrollnumber,employeeid,salary):
        self.id = id
        self.deduction_name = deductionname
        self.deduction_rate = _percentage(deductionrate, 'Deduction rate')
        self.payrollnumber = payrollnumber
        self.employeeid = employeeid
        self.salary = _non_negative_number(salary, 'Salary')
        self.__amount = self.compute_amount()

    def compute_amount(self):
        self.__amount = self.salary * (self.deduction_rate / 100)
        return self.__amount

    def get_amount(self):
        return self.__amount


class Allowance:
    def __init__(self,id,payrollid,employmentid,name,rate):
        self.id = id
        self.payrollid = payrollid
        self.employmentid = employmentid
        self.name = name
        self.rate = _percentage(rate, 'Allowance rate')
        self.__amount = 0

    def compute_amount(self, salary):
        salary = _non_negative_number(salary, 'Salary')
        self.__amount = salary * (self.rate / 100)
        return self.__amount

    def get_amount(self):
        return self.__amount

    def __str__(self):
        return f'Payroll id :{self.payrollid}\nAllowance Id :{self.id}\nEmployee Id :{self.employmentid}\nAllowance Rate :{self.name}\nRate :{self.rate}'




class Payroll:
    def __init__(self, payrollid, payslips=None):
        self.payrollid = payrollid
        self.date = self.calculate_date()
        self.payslips = []
        for payslip in payslips or []:
            self.add_payslip(payslip)

    def calculate_date(self):
        from datetime import datetime
        self.date = datetime.now()
        return self.date

    def caculate_date(self):
        """Keep the original misspelled method working for the current CLI."""
        return self.calculate_date()

    def add_payslip(self, payslip):
        if not isinstance(payslip, Payslip):
            raise TypeError('Payroll only accepts Payslip objects')
        if any(saved.id == payslip.id for saved in self.payslips):
            raise ValueError(f'Payslip {payslip.id} is already in this payroll')
        self.payslips.append(payslip)
        return payslip

    def get_total(self):
        return sum(payslip.get_net() for payslip in self.payslips)

    def get_employees(self):
        return [payslip.employeename for payslip in self.payslips]
    
    def __str__(self):
        return f'Payroll with ID {self.payrollid} has been issued on {self.date}'

class Pay(ABC):
    
    @abstractmethod
    def Payments(self):
        pass

class Payslip(Pay):
    def __init__(self,id,employeename,totaldeductions,totalallowances,hours_worked):
        self.id = id
        self.employeename = employeename
        self.totaldeductions = _non_negative_number(totaldeductions, 'Total deductions')
        self.totalallowances = _non_negative_number(totalallowances, 'Total allowances')
        self.hours_worked = _non_negative_number(hours_worked, 'Hours worked')
        self.__gross = 0
        self.__net = 0

    def __str__(self):
        return (
            f'Payslip ID: {self.id}\n'
            f'Employee: {self.employeename}\n'
            f'Gross: {self.get_gross()}\n'
            f'Deductions: {self.totaldeductions}\n'
            f'Net: {self.get_net()}'
        )

    def set_gross(self, salary):
        salary = _non_negative_number(salary, 'Salary')
        self.__gross = salary + self.totalallowances
        self.compute_net()
        return self.__gross
        
    def get_gross (self):
        return self.__gross 


    def compute_net(self):
        self.__net = self.get_gross() - self.totaldeductions
        return self.__net 
    
    def get_net(self):
        return self.__net

    def Payments(self):
        print(f"Payment details for {self.employeename}")
        print(f"Net salary: {self.get_net()}")
        return self.get_net()
