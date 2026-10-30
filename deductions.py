from cli_helpers import ask_yes_no, read_number, read_text, save_record
from oop_prac import Deductions


def run_deduction_workflow():
    while True:
        deduction = Deductions(
            read_text('Enter deduction ID: '),
            read_text('Enter deduction name: '),
            read_number('Enter deduction rate: ', maximum=100),
            read_text('Enter payroll ID: '),
            read_text('Enter employee ID: '),
            read_number('Enter employee salary: '),
        )

        record = {
            'deduction_id': deduction.id,
            'name': deduction.deduction_name,
            'rate': deduction.deduction_rate,
            'payroll_id': deduction.payrollnumber,
            'employee_id': deduction.employeeid,
            'salary': deduction.salary,
            'amount': deduction.compute_amount(),
        }
        save_record('deductions', record, 'deduction_id')

        if not ask_yes_no('Do you want to add another deduction (y/n)? '):
            break


if __name__ == '__main__':
    run_deduction_workflow()
