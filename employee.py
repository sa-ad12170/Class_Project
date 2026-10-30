from datetime import datetime

from cli_helpers import ask_yes_no, read_number, read_text, save_record
from oop_prac import Employee


def run_employee_workflow():
    while True:
        employee = Employee(
            read_text('Enter employee ID: '),
            read_text('Enter first name: '),
            read_text('Enter last name: '),
            read_number(
                'Enter birth year: ',
                minimum=1900,
                maximum=datetime.today().year,
                integer=True,
            ),
            read_text('Enter department: '),
            read_text('Enter gender: '),
            read_text('Enter status: '),
            read_text('Enter contact: '),
            read_text('Enter village: '),
            read_text('Enter city: '),
            read_text('Enter position: '),
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
        save_record('employees', record, 'employee_id')

        if not ask_yes_no('Do you want to add another employee (y/n)? '):
            break


if __name__ == '__main__':
    run_employee_workflow()
