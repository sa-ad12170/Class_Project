from oop_prac import Employee
from storage import DuplicateRecordError, StorageError, append_record
  

while True :
#user input    
    u_employeeid = input ('Enter employee id : ')
    u_fname = input ('Enter first name  : ')
    u_last = input ('Enter last name   : ')
    u_dateofbirth = int(input('Enter birth year : '))
    u_department = input('Enter department : ')
    u_gender = input('Enter gender : ')
    u_status = input('Enter status : ')
    u_contact = input('Enter contact : ')
    u_position = input('Enter position : ')
    u_village = input('Enter village: ')
    u_city = input('Enter city : ')
    
    
    
    

    employee = Employee(u_employeeid,u_fname,u_last ,u_dateofbirth,u_department,u_gender ,u_status,u_contact ,u_village,u_city,u_position) 
    


    new_employee = {
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
    try:
        append_record('employees', new_employee, 'employee_id')
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)

        
    add_employee = input ('Do you want to add employee  (y/n) :')    

    if  add_employee == 'y' :
        continue 
    else :
        break
