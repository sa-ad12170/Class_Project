from cli_helpers import ask_yes_no, read_text, save_record
from oop_prac import Payroll


def run_payroll_workflow():
    while True:
        payroll = Payroll(read_text('Enter payroll ID: '))
        print(payroll)

        record = {
            'payroll_id': payroll.payrollid,
            'issued_at': payroll.date.isoformat(),
        }
        save_record('payrolls', record, 'payroll_id')

        if not ask_yes_no('Do you want to add another payroll (y/n)? '):
            break


if __name__ == '__main__':
    run_payroll_workflow()
