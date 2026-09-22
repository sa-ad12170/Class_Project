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
          

