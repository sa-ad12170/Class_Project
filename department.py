
                         
from oop_prac import Department

data = {}

departments = {}
number = int(input('how many departments do you want to add : '))
for i in range(number ):
    dept_id = input('Enter department id :')
    dept_name = input('Enter department name :')
    #no_of_staff = input('Enter no of staff :')

    department = Department(dept_id,dept_name)

         

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
        dept_id = input ('enter department id :') 
        if department_id in departments : 
            employeeid = input ('enter staff  id  to remove :')
            departments[dept_id].remove_staff(employeeid)
            print("staff removed sucessfully ")
        else :
            print('Department not found ')
      
#display staff 
      
    elif choice == '3':
        dept_id = input ('Enter department id : ')
        if dept_id in departments :
            departments[dept_id].display_staff()
        else :
            print ('Department not found ') 
#count staff 
    elif choice  == '4'  : 
        department_id = input ('Enter department id : ')
        if dept_id in departments : 
            number = departments[department_id].get_no_of_staff()
            print(f'Number of staff in department : {number}')
        else :
            print ('Department not found ') 

    elif choice == '5':
        #break
        print ('Exited')  
        break
    else :
        print ('Invalid option')         

 





   

