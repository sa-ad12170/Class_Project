from cli_helpers import ask_yes_no, read_number, read_text, save_record
from oop_prac import Salary


def run_salary_workflow():
    while True:
        salary = Salary(
            read_text('Enter employee ID: '),
            read_number('Enter hours worked: '),
            read_number('Enter hourly rate: '),
        )
        print(f'Salary: {salary.get_salary()}')

        record = {
            'employee_id': salary.employee_id,
            'hours_worked': salary.hoursworked,
            'rate_per_hour': salary.rateperhour,
            'salary': salary.get_salary(),
        }
        save_record('salaries', record, 'employee_id')

        if not ask_yes_no('Do you want to add another salary (y/n)? '):
            break


if __name__ == '__main__':
    run_salary_workflow()
