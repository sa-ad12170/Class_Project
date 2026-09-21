

from oop_prac import Employee
import json


try:
    with open ('employee.json','r') as file :
            employees = json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    employees= []
  

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
    
    
    
    

    employee = Employee(u_employeeid,u_fname,u_last ,u_dateofbirth,u_department,u_gender ,u_status,u_contact ,u_village,u_city) 
    


    new_employee = {
        'employeeid' : employee.id,
        'First name ' :  employee.firstname,
        'Last name ' : employee.lastname,
        'Birth year' : employee.dateofbirth,
        'Department' : employee.department,
        'Gender' : employee.gender,
        'Status' : employee.status,
        'Position' : employee.position,
        'Contact' : employee.contact,
        'Address' : employee.get_address(),
        'Age'     :employee.get_age(),
        
    }

    
        

    with open ("employee.json",'w') as file :
            employees.append(new_employee)
            json.dump( employees,file, indent = 4)

        
    add_employee = input ('Do you want to add employee  (y/n) :')    

    if  add_employee == 'y' :
        continue 
    else :
        break 