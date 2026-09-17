from oop_prac import Department
import json
#DeptID,Name,Number_of_staff
depart = []


while True :
#user input    
    u_deptid = input ('Enter department id :')
    u_name = input ('Enter department name  :')
    u_staff = int(input ('Enter number of staff  :'))

    department = Department(u_deptid,u_name,u_staff)

    new_dept = {
        'department_id' : department.deptid,
        'department_name': department.name,
        'number_of_staff':department.number_of_staff
    }

    with open ("dept.json",'w') as file :
            depart.append(new_dept)
            json.dump( new_dept,file, indent = 4)
    
    with open ('dept.json','r') as file :
        
        depart = json.load(file)

   
    add_depat = input ('Do you want to add another department (y/n) :')    

    if  add_depat == 'y' :
        continue 
    else :
        break 