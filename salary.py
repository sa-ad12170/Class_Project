from oop_prac import Salary
import json 
try:
    with open ('salary.json','r') as file :
            salaries = json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    salaries = []

while True:
    u_employee_id = input ('Enter employee id : ')
    u_hoursworked = int(input ('Enter hoursworked :'))
    u_rate =int( input ('Enter rate :'))

    salary = Salary(u_employee_id,u_hoursworked,u_rate)
    paidsalary = salary.get_salary()
    print(f'SALARY : {paidsalary}')

    new_dedecution = {
            'Employee_id' : salary.employee_id,
            'hours_worked': salary.hoursworked,
            'Hour_rate':salary.rateperhour,
            'Salary ' : salary.get_salary(),
            
        }
    with open ("salary.json",'w') as file :
                salaries.append(new_dedecution)
                json.dump(salaries,file, indent = 4)
        
    
    add_salary = input ('Do you want to add another employees salary  (y/n) :')    

    if  add_salary == 'y' :
            continue 
    else :
            break 