from cli_helpers import read_text
from oop_prac import Department
from storage import StorageError, load_records, save_records


def load_departments():
    departments = {}
    for saved_department in load_records('departments'):
        department = Department(
            saved_department['department_id'],
            saved_department['name'],
        )
        department.staff = saved_department.get('staff', [])
        departments[department.deptid] = department

    if not departments:
        departments = {
            'dept001': Department('dept001', 'IT'),
            'dept002': Department('dept002', 'Sales'),
        }
    return departments


def save_departments(departments):
    save_records(
        'departments',
        [department.to_dict() for department in departments.values()],
    )


def choose_department(departments):
    department_list = list(departments.values())
    print('\nAvailable departments:')
    for number, department in enumerate(department_list, start=1):
        print(f'{number}. {department.departmentname}')

    choice = input('Select a department number: ').strip()
    if choice.isdigit() and 1 <= int(choice) <= len(department_list):
        return department_list[int(choice) - 1]

    print('Invalid department selection')
    return None


def run_department_menu():
    try:
        departments = load_departments()
    except StorageError as error:
        print(error)
        return

    while True:
        print('\nDEPARTMENT MENU')
        print('1. Add staff')
        print('2. Remove staff')
        print('3. Display staff')
        print('4. Count staff')
        print('5. Return to main menu')
        choice = input('Enter your choice: ').strip()

        if choice == '1':
            department = choose_department(departments)
            if department is None:
                continue

            employee = {
                'employee_id': read_text('Enter employee ID: '),
                'name': read_text('Enter staff name: '),
                'position': read_text('Enter position: '),
            }
            try:
                department.add_staff(employee)
                save_departments(departments)
                print('Staff member added successfully')
            except (ValueError, StorageError) as error:
                print(error)

        elif choice == '2':
            department_id = read_text('Enter department ID: ')
            if department_id not in departments:
                print('Department not found')
                continue

            employee_id = read_text('Enter staff ID to remove: ')
            result = departments[department_id].remove_staff(employee_id)
            try:
                save_departments(departments)
                print(result)
            except StorageError as error:
                print(error)

        elif choice == '3':
            department_id = read_text('Enter department ID: ')
            if department_id in departments:
                departments[department_id].display_staff()
            else:
                print('Department not found')

        elif choice == '4':
            department_id = read_text('Enter department ID: ')
            if department_id in departments:
                number = departments[department_id].get_no_of_staff()
                print(f'Number of staff in department: {number}')
            else:
                print('Department not found')

        elif choice == '5':
            try:
                save_departments(departments)
                print('Returning to main menu')
            except StorageError as error:
                print(error)
            return

        else:
            print('Invalid option')


if __name__ == '__main__':
    run_department_menu()

