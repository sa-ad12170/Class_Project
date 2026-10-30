from cli_helpers import ask_yes_no, read_number, read_text, save_record
from oop_prac import Payslip


def run_payslip_workflow():
    while True:
        payslip = Payslip(
            read_text('Enter payslip ID: '),
            read_text('Enter employee name: '),
            read_number('Enter total deductions: '),
            read_number('Enter total allowances: '),
            read_number('Enter hours worked: '),
        )
        payslip.set_gross(read_number('Enter salary: '))
        print(payslip)
        payslip.Payments()

        record = {
            'payslip_id': payslip.id,
            'employee_name': payslip.employeename,
            'total_deductions': payslip.totaldeductions,
            'total_allowances': payslip.totalallowances,
            'hours_worked': payslip.hours_worked,
            'gross': payslip.get_gross(),
            'net': payslip.get_net(),
        }
        save_record('payslips', record, 'payslip_id')

        if not ask_yes_no('Do you want to add another payslip (y/n)? '):
            break


if __name__ == '__main__':
    run_payslip_workflow()
