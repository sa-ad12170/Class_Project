from cli_helpers import ask_yes_no, read_number, read_text, save_record
from oop_prac import Allowance


def run_allowance_workflow():
    while True:
        allowance = Allowance(
            read_text('Enter allowance ID: '),
            read_text('Enter payroll ID: '),
            read_text('Enter employee ID: '),
            read_text('Enter allowance name: '),
            read_number('Enter allowance rate: ', maximum=100),
        )
        print(allowance)

        record = {
            'allowance_id': allowance.id,
            'payroll_id': allowance.payrollid,
            'employee_id': allowance.employmentid,
            'name': allowance.name,
            'rate': allowance.rate,
        }
        save_record('allowances', record, 'allowance_id')

        if not ask_yes_no('Do you want to add another allowance (y/n)? '):
            break


if __name__ == '__main__':
    run_allowance_workflow()
