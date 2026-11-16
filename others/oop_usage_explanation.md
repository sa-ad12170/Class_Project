# Where Object-Oriented Programming Is Used

This document explains how the project uses OOP (Object-Oriented Programming). The main class definitions are in `oop_prac.py`; `main.py` creates and uses their objects. This is an explanation only; no program code has been changed.

## 1. Classes and objects

A **class** is a description of the information and actions for a type of thing. An **object** is one particular instance created from that class.

For example, `Employee` is a class in `oop_prac.py` (around line 135). When `main.py` collects employee details, it creates an employee object:

```python
employee = Employee(..., position, tax_resident)
```

That object holds the details for one particular employee. The project also creates objects from `Department`, `Position`, `Allowance`, `Deductions`, `Payslip`, and `Payroll`.

## 2. Encapsulation: keeping related data and operations together

**Encapsulation** means placing related data and the operations that use that data in the same class. For instance:

- `Employee` keeps a person's name, date of birth, contact details, status, and position. Its methods and properties provide values such as `full_name`, `age`, `department`, and `salary` (`oop_prac.py`, around lines 135–229).
- `Deductions` holds salary and allowance amounts and calculates NSSF and PAYE (`oop_prac.py`, around lines 232–285).
- `Payroll` holds the payslips for a run and calculates totals from those slips (`oop_prac.py`, around lines 314–377).
- `Allowance` holds the allowance ID, employee ID, name, and amount (`oop_prac.py`, around lines 288–311).

The fields are public Python attributes such as `employee.firstname` and `employee.position`; the project does not hide them with private access controls. So encapsulation here mainly means that each class groups the information and its related behavior. It is not strict data hiding.

`Employee` also uses `@property` for calculated values. For example, reading `employee.salary` returns `employee.position.salary` (`oop_prac.py`, around lines 183–189). That avoids storing a second salary value on the employee that could get out of sync with the position.

## 3. Composition: objects made from or containing other objects

**Composition** is a “has-a” relationship: one object contains or holds another object as one of its parts.

### Employee has a Position

In `main.py`, a `Position` object is made and passed into the `Employee` constructor. `Employee.__init__` stores it as `self.position` (`oop_prac.py`, around line 147). The employee uses that position for its department and salary:

```python
employee.position.title
employee.department   # reads position.department
employee.salary       # reads position.salary
```

So the employee object has a position object.

### Payroll has Payslips

`Payroll.__init__` receives a list of payslip objects and stores it as `self.payslips` (`oop_prac.py`, around lines 314–318). Its total properties loop through those payslip objects to add up gross pay, deductions, employer NSSF, or net pay (`oop_prac.py`, around lines 334–360). So a payroll object has a collection of payslip objects.

### Two important details

- Department staff are saved as dictionaries: `main.py` calls `employee.to_dict()` and passes that record to `department.add_staff(...)`. The department's `staff` list therefore contains saved records, not `Employee` objects. That is not a direct Department-to-Employee object composition in the current code.
- `Payslip` receives an employee, allowance objects, and a deductions object, but it copies the needed values into its own fields. For example, it saves `employee.full_name` and `deductions.paye`; it does not keep those original objects as attributes. This is object use during construction, while the lasting Payroll-to-Payslip relationship is the clearer composition example.

## 4. Inheritance: a class extending another class

**Inheritance** lets a class take a shared interface or behavior from a parent class. `Pay` is an abstract parent class (`oop_prac.py`, around lines 380–385). `Payslip` inherits from it:

```python
class Payslip(Pay):
```

This says that `Payslip` is a kind of `Pay` for purposes of the class relationship. In this project, this inheritance is small: `Pay` defines one required method, `Payments`.

## 5. Abstraction: describing a required action without implementing it

`Pay` inherits from Python's `ABC` base class and marks `Payments` with `@abstractmethod` (`oop_prac.py`, around lines 380–385). An abstract method declares what a child class must provide, without specifying the actual work.

Here, `Pay` says that a concrete payment class must provide `Payments()`. `Payslip` provides that method. This is the project's use of abstraction: code can define a general payment contract without describing all possible payment details in the parent class.

## 6. Polymorphism: the same method name can do class-specific work

**Polymorphism** means that different classes can provide their own implementation of the same method, and code can call that method through a common interface.

`Pay` requires `Payments()`, and `Payslip` implements it near the end of `oop_prac.py` (around lines 458–459):

```python
def Payments(self):
    self.display()
```

That implementation displays the payslip. This is a basic polymorphic setup through the `Pay` interface. In the current program, `main.py` calls `Payslip.display()` directly; it does not call `Payments()` through a `Pay` reference. There is also only one concrete `Pay` subclass at present, so polymorphism is present in the class design but is not widely exercised by the current workflow.

## 7. Class methods: actions that work with the class

A `@classmethod` receives the class itself as `cls`, rather than a particular object as `self`. The project uses class methods for tasks that apply to the class or its saved collection:

- `Employee.generate_id()` finds the next employee ID (`oop_prac.py`, around lines 154–170).
- `Allowance.generate_id()` creates an allowance ID (`oop_prac.py`, around lines 299–303).
- `Payroll.generate_id()` creates the next payroll ID (`oop_prac.py`, around lines 320–332).
- `SalaryScale.load()`, `save()`, and `get_salary()` work with shared salary scale data (`oop_prac.py`, around lines 84–114).
- `from_dict()` class methods recreate objects from saved dictionaries, such as `Employee.from_dict(...)` and `Department.from_dict(...)`.

For example, `Employee.generate_id()` is called as `Employee.generate_id()` in `main.py`. It does not need an existing employee object to generate an ID.

## 8. Saving and loading objects

JSON stores basic data such as dictionaries, lists, strings, and numbers; it does not directly store Python class instances. The classes provide conversion methods:

- `to_dict()` converts an object to a dictionary that can be written into JSON.
- `from_dict()` builds an object again from a saved dictionary.

For example, `employee.to_dict()` is stored in the department's `staff` list. Later, `Employee.from_dict(record, position)` turns that record back into an `Employee` object. The saved JSON data is therefore the stored form; the Python objects are rebuilt when the program loads and uses the records.

## 9. How `main.py` coordinates the objects

`main.py` mostly contains ordinary functions that manage the program flow and user input. These functions create objects and ask them to do their jobs. During a payroll run, the general flow is:

1. Load employee records and build `Employee` objects, each with a `Position` object.
2. Load the employee's `Allowance` objects.
3. Create a `Deductions` object to calculate NSSF and PAYE.
4. Create one `Payslip` object for each employee.
5. Put those payslips into a `Payroll` object, which calculates the run totals.
6. Convert the payroll to dictionaries and save them in `data.json`.

This division lets `main.py` handle the conversation with the user, while the model classes hold related payroll information and calculations.

## Quick summary

| OOP idea | Where it appears |
| --- | --- |
| Classes and objects | `Department`, `Employee`, `Position`, `Allowance`, `Deductions`, `Payslip`, and `Payroll` in `oop_prac.py` |
| Encapsulation | Each class groups its relevant data and methods; `Employee` properties provide calculated values |
| Composition | `Employee` stores a `Position`; `Payroll` stores a list of `Payslip` objects |
| Inheritance | `Payslip` extends `Pay` |
| Abstraction | `Pay` declares the abstract `Payments()` method |
| Polymorphism | `Payslip` implements `Payments()`; current main workflow calls `display()` directly |
| Class methods | ID generation, salary scale operations, and object reconstruction from dictionaries |
