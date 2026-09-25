from oop_prac import Position
import json
positions =[]
while True :
    u_title = input ("Enter title : ")
    u_department = input ("enter department : ") 
    u_salary =  input ('Enter salary ')

    position = Position (u_title,u_department,u_salary)
    print()
    print ('\t++++++POSITION DETAILS++++++')
    print (position)



    new_position = {
            'Title' : position.title,
            'Department' :  position.department,
            'Salary' : position.salary,   
        }
    positions.append(new_position)

    with open ('position.json','w') as file :
        json.dump(positions,file,indent=4)

    with open ('positions.json','r') as file :
        positions = json.load(file)   

    add_position = input ('Do you want to add another position (y/n) : ')    
    
    if  add_position == 'y' :
            continue 
    else :
            break     