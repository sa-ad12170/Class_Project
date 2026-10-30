from oop_prac import Salary
from storage import DuplicateRecordError, StorageError, append_record

while True:
    u_employee_id = input ('Enter employee id : ')
    u_hoursworked = int(input ('Enter hoursworked :'))
    u_rate =int( input ('Enter rate :'))

    salary = Salary(u_employee_id,u_hoursworked,u_rate)
    paidsalary = salary.get_salary()
    print(f'SALARY : {paidsalary}')

    new_salary = {
        'employee_id': salary.employee_id,
        'hours_worked': salary.hoursworked,
        'rate_per_hour': salary.rateperhour,
        'salary': salary.get_salary(),
    }
    try:
        append_record('salaries', new_salary, 'employee_id')
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)
        
    
    add_salary = input ('Do you want to add another employees salary  (y/n) :')    

    if  add_salary == 'y' :
            continue 
    else :
            break
