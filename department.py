from oop_prac import Department
from storage import load_records, save_records


def load_departments():
    saved_departments = load_records('departments')

    departments = {}
    for saved_department in saved_departments:
        department = Department(
            saved_department['department_id'],
            saved_department['name'],
        )
        department.staff = saved_department.get('staff', [])
        departments[department.deptid] = department

#this is implelemted when the departments dictionary is empty it will execute the default and if you want to hard code it eraseS the json and then try to run again

    if not departments:
        departments = {
            'dept001': Department('dept001', 'IT'),
            'dept002': Department('dept002', 'Sales'),
        }

    return departments

#this is a one oline statment the brackets mean put the values in the brackets outcome comes first and then the loop follows
def save_departments(departments):
    save_records(
        'departments',
        [department.to_dict() for department in departments.values()],
    )


departments = load_departments()


def choose_department():
    department_list = list(departments.values())
    print('\nAvailable departments:')
    for number, department in enumerate(department_list, start=1):
        print(f'{number}.{department.departmentname}')

    choice = input('Select a department number: ')
    if choice.isdigit() and 1 <= int(choice) <= len(department_list):
        return department_list[int(choice) - 1]

    print('Invalid department selection')
    return None

def run_department_menu():
    while True:
        print('\t\tMENU\n1.Add staff\n2.Remove staff\n3.Display staff\n4.Count staff\n5.Exit')
        choice = input('Enter your choice : ')

        if choice == '1':
            department = choose_department()
            if department is not None:
                name = input('Enter staff name : ')
                employeeid = input('Enter employee id : ')
                position = input('Enter position : ')
                employee = {
                    'employee_id': employeeid,
                    'name': name,
                    'position': position,
                }
                try:
                    department.add_staff(employee)
                    save_departments(departments)
                    print('Staff member added successfully')
                except ValueError as error:
                    print(error)
            else:
                print('Department not found')

        elif choice == '2':
            dept_id = input('Enter department id: ')
            if dept_id in departments:
                employeeid = input('Enter staff id to remove: ')
                result = departments[dept_id].remove_staff(employeeid)
                save_departments(departments)
                print(result)
            else:
                print('Department not found')

        elif choice == '3':
            dept_id = input('Enter department id: ')
            if dept_id in departments:
                departments[dept_id].display_staff()
            else:
                print('Department not found')

        elif choice == '4':
            department_id = input('Enter department id: ')
            if department_id in departments:
                number = departments[department_id].get_no_of_staff()
                print(f'Number of staff in department: {number}')
            else:
                print('Department not found')

        elif choice == '5':
            save_departments(departments)
            print('Exited')
            break

        else:
            print('Invalid option')


if __name__ == '__main__':
    run_department_menu()
   
