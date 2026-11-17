# Flask Front End Guide

This guide explains the web pages in this project, how Flask connects them to the existing Python files, and what happens when a user submits a form. The code is kept in one Flask file and simple HTML templates so it is easier to follow while learning.

## 1. How a web request moves through the project

The browser displays an HTML page. When a person opens a link or submits a form, the browser sends a request to Flask. Flask runs a route function in `app.py`. That function calls the existing Python classes and helper functions, then either saves data or asks Flask to display an HTML template.

```text
Browser page
    -> Flask route in app.py
        -> existing Python classes and helper modules
            -> data.json
        <- values returned to the route
    <- HTML template rendered for the browser
```

For example, adding a department follows this flow:

1. The browser sends the department name from the HTML form.
2. Flask reads it with `request.form.get("name")`.
3. The route calls `Department.add_department(...)` to validate and add it.
4. `save_departments(...)` stores it through `data_store.py`.
5. Flask redirects the browser to the department list.

## 2. Project files used by Flask

| File | What it contains | Why the Flask app uses it |
|---|---|---|
| `app.py` | Flask routes and request handling | Connects browser URLs and form submissions to Python code. |
| `templates/base.html` | Shared page structure and top navigation | Keeps the same header and links on every page. |
| `templates/departments.html` | Department form and table | Shows and adds departments. |
| `templates/employees.html` | Employee form and table | Adds employees, lists them, and provides removal forms. |
| `templates/payroll_roster.html` | Active roster table | Displays employees currently included in payroll. |
| `templates/allowances.html` | Allowance form and table | Adds an allowance for an employee and lists saved allowances. |
| `templates/salary_scale.html` | Salary table and update form | Shows and updates the saved pay amount for each position. |
| `templates/payrolls.html` | Payroll run form and history table | Starts payroll calculations and lists saved runs. |
| `templates/payslips.html` | Payslip search and details | Filters saved payslips by payroll ID or employee ID. |
| `department.py` | Department load and save helpers | Turns saved department records into `Department` objects and saves them back. |
| `data_store.py` | JSON storage helpers | Reads and writes sections in `data.json` while preserving the other sections. |
| `oop_prac.py` | Main project classes and validation | Supplies objects such as `Employee`, `Department`, `Allowance`, `Payroll`, and `Payslip`. |
| `main.py` | Existing command-line helpers | Flask reuses `load_employees` and `sync_payroll_roster` from it. |
| `data.json` | Saved application records | Holds departments, salaries, allowances, roster data, and payroll history. |

The templates folder must be named exactly `templates`. Flask searches that folder when `render_template(...)` is called.

## 3. Flask setup and shared helpers

At the top of `app.py`, these imports connect the Flask layer with the project backend:

```python
from flask import Flask, redirect, render_template, request, url_for

from data_store import load_records, save_records
from department import load_departments, save_departments
from main import load_employees, sync_payroll_roster
from oop_prac import (Allowance, Department, Deductions, Employee, Payroll,
                      Payslip, Position, SalaryScale)

app = Flask(__name__)
```

- `Flask` creates the web application.
- `request` gives a route access to submitted form values.
- `render_template` fills an HTML template with Python values.
- `redirect` sends the browser to another route after a successful change.
- `url_for` builds a URL from a route function's name.
- The imports from the project files reuse the existing data rules and payroll calculations.

The helper `get_salary_scale()` fills any missing saved position with the project's default salary. `get_employees()` uses the shared employee loader to rebuild saved employee dictionaries as `Employee` objects:

```python
def get_salary_scale():
    scale = SalaryScale.defaults()
    scale.update(SalaryScale.load())
    return scale


def get_employees():
    scale = get_salary_scale()
    return scale, load_employees(scale)
```

The existing employee records are stored inside each department in `data.json`. `main.load_employees(scale)` reads those records and uses `Employee.from_dict(...)` and `Position` to make useful Python objects. The templates can then display values such as `employee.full_name` and `employee.salary`.

## 4. Routes and navigation

A route connects a URL and an HTTP method to a Python function. For example:

```python
@app.route("/departments")
def departments_page():
    departments = load_departments()
    return render_template("departments.html", departments=departments)
```

When the browser requests `/departments`, Flask runs `departments_page()`. The helper returns department objects; `render_template` makes them available to `departments.html` under the name `departments`.

The shared navigation is in `base.html`:

```html
<nav>
    <a href="{{ url_for('departments_page') }}">Departments</a>
    <a href="{{ url_for('employees') }}">Employees</a>
    <a href="{{ url_for('payroll_roster') }}">Payroll roster</a>
    <a href="{{ url_for('allowances') }}">Allowances</a>
    <a href="{{ url_for('salary_scale') }}">Salary scale</a>
    <a href="{{ url_for('payrolls') }}">Run payroll</a>
    <a href="{{ url_for('payslips') }}">Payslips</a>
</nav>
```

`url_for('employees')` means “make the URL for the route whose Python function is named `employees`.” This avoids manually repeating paths in links.

Each page starts with a Jinja template instruction such as:

```html
{% extends "base.html" %}
```

This means the page reuses the shared header and provides its own content inside `{% block content %}...{% endblock %}`. Jinja is the small template language Flask uses to insert data and repeat HTML.

## 5. Forms, tables, and Jinja

### A department form

```html
<form action="{{ url_for('add_department') }}" method="post">
    <label for="name">Department name:</label>
    <input type="text" id="name" name="name" required>
    <button type="submit">Add department</button>
</form>
```

- `action` tells the browser which Flask route should receive the form.
- `method="post"` sends data intended to create or update something.
- `name="name"` gives the submitted value a key that Flask can read.
- `required` asks the browser to require a value before submitting.

The matching Flask code reads that key and calls existing backend code:

```python
name = request.form.get("name", "")
Department.add_department(departments, name)
save_departments(departments)
```

`Department.add_department` checks for an empty or duplicate name. `save_departments` converts department objects to dictionaries with `to_dict()` and passes them to `data_store.save_records(...)`.

### A table and loop

```html
{% for department in departments %}
    <tr>
        <td>{{ department.deptid }}</td>
        <td>{{ department.departmentname }}</td>
        <td>{{ department.get_no_of_staff() }}</td>
    </tr>
{% else %}
    <tr><td colspan="3">No departments found.</td></tr>
{% endfor %}
```

`{% for ... %}` repeats the row for each department. `{{ ... }}` displays a value. The optional `{% else %}` displays a row when the list is empty. Other tables use the same pattern for employees, allowances, payroll runs, and payslips.

### GET and POST

The employee and allowance pages use routes that accept both methods:

```python
@app.route("/employees", methods=["GET", "POST"])
def employees():
    if request.method == "POST":
        # Read the form and save a new employee.

    # Load employees and display the page.
```

`GET` means display the page. `POST` means process a form submission. This lets one URL show a form/table and receive its form.

After a successful POST, a route usually redirects to a GET page. That refreshes the data shown in the browser and avoids resubmitting the form if the page is refreshed.

## 6. How each section uses the backend

### Departments

- `department.load_departments()` reads the `departments` JSON section and builds `Department` objects with `Department.from_dict(...)`.
- `Department.add_department(...)` validates and adds a department.
- `department.save_departments(...)` converts those objects back to dictionaries and saves them.

### Employees

- The form collects the same basic details used by `Employee` in `oop_prac.py`: name, date of birth, contact, address, gender, status, position, and tax residency.
- `Employee.generate_id()` chooses the next employee ID.
- `Position(...)` connects the selected position and department with its salary.
- `Employee(...)` validates and creates the object; `employee.to_dict()` turns it into a JSON-friendly record.
- The record is saved in the selected department's `staff` list using `save_departments(...)`.
- `main.load_employees(scale)` reconstructs saved records as `Employee` objects for the list page.

Employee removal deletes the employee record and the associated allowances, roster row, and saved payslips. Payroll totals are recalculated after matching payslips are removed, following the existing command-line behavior.

### Payroll roster

`main.sync_payroll_roster(scale)` finds active employees, saves their roster entries in the `payroll_roster` data section, and returns the list for the HTML table.

### Allowances

- The form selects an employee and sends an allowance name and amount.
- `Allowance.generate_id()` creates an ID.
- `Allowance(...)` validates the name and amount.
- `Allowance.to_dict()` creates the record saved in the `allowances` section.

### Salary scale

- `SalaryScale.load()` reads stored position salaries.
- `SalaryScale.save(scale)` validates and saves the updated values.
- `Position.TITLES` supplies the allowed position names, so the form uses the same choices as the backend.

### Payroll runs

The route uses the existing payroll classes instead of asking the terminal for values:

1. It checks the submitted date with Python's `date.fromisoformat(...)`.
2. It loads active employees and saved allowances.
3. `Deductions(...)` calculates deductions using the existing rules in `oop_prac.py`.
4. `Payslip(...)` creates one saved result for each employee.
5. `Payroll(...)` collects the payslips and calculates payroll totals.
6. `payroll.to_dict()` converts the result to JSON-friendly data and `save_records("payrolls", ...)` saves it.

### Payslips

The payslip page reads saved payroll records and uses `Payslip.from_dict(...)` to create payslip objects. The search form uses GET, so the IDs appear in the URL, for example `/payslips?payroll_id=PR001&employee_id=Emp001`.

## 7. Why the command-line program is not called directly

`main.py` includes functions that call `input()` and `print()`. Those functions wait for someone to type into the terminal, which is not how a browser form works. The Flask routes read the browser's submitted values with `request.form`, then call the reusable backend classes and storage helpers.

The Flask app imports `load_employees` and `sync_payroll_roster` from `main.py`. The command-line menu is protected by:

```python
if __name__ == "__main__":
    main()
```

Therefore importing `main.py` gives Flask access to those helper functions without starting the command-line menu.

## 8. Running the application

From the project folder, run:

```powershell
py app.py
```

Open the local address Flask prints in the terminal. Keep the terminal running while using the site. Stop the server with `Ctrl+C` in that terminal.

## 9. A simple example from form to saved record

Suppose a user enters `Research` into the department form and clicks **Add department**.

The browser sends a POST request to `/departments/add`. Flask gets the text using:

```python
name = request.form.get("name", "")
```

Then the backend creates and validates the object:

```python
Department.add_department(departments, name)
```

Finally, the helper saves the updated departments to the `departments` section in `data.json`:

```python
save_departments(departments)
```

The route redirects the browser to the list page, which loads the saved data and displays it as a table row.

## 10. Learning notes

- Flask routes are Python functions attached to URLs.
- HTML forms send user input to routes.
- `request.form` reads submitted values.
- `render_template` sends Python values into HTML.
- Jinja expressions `{{ value }}` display values; Jinja loops `{% for ... %}` build repeated table rows.
- Existing classes hold business rules; the Flask app connects browser input to those rules.
- `data_store.py` is the single place that reads and writes the JSON sections.
