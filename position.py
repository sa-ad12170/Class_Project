from oop_prac import Position
from storage import DuplicateRecordError, StorageError, append_record

while True :
    u_title = input ("Enter title : ")
    u_department = input ("enter department : ") 
    u_salary =  input ('Enter salary ')

    position = Position(u_title,u_department,u_salary)
    
    print ('\t++++++POSITION DETAILS++++++')
    #print (position)

    new_position = {
        'title': position.title,
        'department': position.department,
        'salary': position.salary,
        'status': position.status(),
    }
    try:
        append_record('positions', new_position, ('title', 'department'))
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)

    add_position = input ('Do you want to add another position (y/n) : ')    
    
    if  add_position == 'y' :
            continue 
    else :
            break
