from allowance import run_allowance_workflow
from deductions import run_deduction_workflow
from department import run_department_menu
from employee import run_employee_workflow
from payroll import run_payroll_workflow
from payslip import run_payslip_workflow
from position import run_position_workflow
from salary import run_salary_workflow


MENU_OPTIONS = {
    '1': ('Allowance', run_allowance_workflow),
    '2': ('Deductions', run_deduction_workflow),
    '3': ('Salary', run_salary_workflow),
    '4': ('Payroll', run_payroll_workflow),
    '5': ('Payslip', run_payslip_workflow),
    '6': ('Position', run_position_workflow),
    '7': ('Employee', run_employee_workflow),
    '8': ('Department', run_department_menu),
}


def display_menu():
    print('\nPAYROLL SYSTEM')
    for number, (name, _) in MENU_OPTIONS.items():
        print(f'{number}. {name}')
    print('9. Exit')


def main():
    while True:
        display_menu()
        try:
            option = input('Enter option: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting payroll system')
            return

        if option == '9':
            print('Exiting payroll system')
            return

        selected = MENU_OPTIONS.get(option)
        if selected is None:
            print('Invalid option')
            continue

        _, workflow = selected
        workflow()


if __name__ == '__main__':
    main()
