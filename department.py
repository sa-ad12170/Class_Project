'''
from oop_prac import Department
import json
#DeptID,Name,Number_of_staff
print ("\tMenu\n1.Add department\n2.Add staff\n3.Remove Staff\n4.Display Staff")
option = input('Enter option : ')
depart = []
if option == '1':
    try:
        with open ('dept.json','r') as file :
                depart = json.load(file)


    except FileNotFoundError:
        print("File not found. Creating a new file.")
        depart = []


    while True :
    #user input    
        u_deptid = input ('Enter department id :')
        u_name = input ('Enter department name  :')
        u_staff = int(input ('Enter number of staff  :'))

        department = Department(u_deptid,u_name,u_staff)          #question to be raised


        new_dept = {
            'department_id' : department.deptid,
            'department_name': department.name,
            'number_of_staff':department.number_of_staff
        }
    
        depart.append(new_dept)  

        with open ("dept.json",'w') as file :
                
                json.dump( depart,file, indent = 4)

        add_depat = input ('Do you want to add another department (y/n) :')    

        if  add_depat == 'y' :
            continue 
        else :
            break 

elif option == "2" :
    try:
            with open ('dept.json','r') as file :
                    staff = json.load(file)
    
    
    except FileNotFoundError:
            print("File not found. Creating a new file.")
            staff = []
    for department in depart :
          f_name  = input ('Enter first name :')
          l_name = input ('Enter last name : ')
          depart_name = input ('Enter department name : ')
          new_staff = {
             "First Name " : f_name,
             "Last name " : l_name,
             "Department" : depart_name
        } 
          staff.append(new_staff) 

          with open ("dept.json",'w') as file :
                        
            json.dump( depart,file, indent = 4)
        
          add_depat = input ('Do you want to add another department (y/n) :')    
        
          if  add_depat == 'y' :
                    continue 
          else :
                    break   
'''                           
from oop_prac import Department
departments = {}
number = int(input('how many departments do you want to add : '))
for i in range(number ):
    dept_id = input('Enter department id :')
    dept_name = input('Enter department name :')
    #no_of_staff = input('Enter no of staff :')

    department = Department(dept_id,dept_name)

    departments[dept_id] = department

while True : 
    print ('\t\tMENU\n1.Add staff\n2.Remove staff\n3.Display staff\n4.Count staff\n5.Exit ')
    choice = input('Enter your choice : ')
    #add staff
    if choice == '1':
        dept_id = input ('Enter department id : ')
        if dept_id in departments : 
            name = input ('Enter staff name id : ')
            employeeid = input ('Enter employee id : ')
            position = input ('Enter position : ')
            employee = {
                'id' : employeeid,
                'name' : name,
                'position' : position
            }
        departments[dept_id].add_staff(employee)  
        print('staff member added sucessfully' ) 
#remove staff 
    elif choice == '2' :
        department_id = input ('enter department id :') 
        if department_id in departments : 
            employeeid = input ('enter staff  id  to remove :')
            departments[dept_id].remove_staff(employeeid)
            print("staff removed sucessfully ")
        else :
            print('Department not found ')
      
#display staff 
      
    elif choice == '3':
        department_id = input ('Enter department id : ')
        if department_id in departments :
            departments[dept_id].display_staff()
        else :
            print ('Department not found ') 
#count staff 
    elif choice  == '4'  : 
        department_id = input ('Enter department id : ')
        if department_id in departments : 
            number = departments[department_id].get_no_of_staff()
            print(f'Number of staff in department : {number}')
        else :
            print ('Department not found ') 
    elif choice == 5 :
        print ('Exiting')  
        break
    else :
        print ('Invalid option')         

 





   

