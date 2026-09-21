
# need to make the rate automatic 

from oop_prac import Deductions
import json
#DeptID,Name,Number_of_staff

try:
    with open ('deduction.json','r') as file :
            dedcutions = json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    dedcutions= []


while True :
#user input    
    u_dedcutionid = input ('Enter decution id :')
    u_decname = input ('Enter decution name  :')
    u_rate = int(input ('Enter rate of deduction  :'))
    u_payrollno = input ('Enter pay roll number  :')
    u_employeeid = input ('Enter employee id  :')
    u_hours = int(input('Enter hours worked : '))
    u_rateperhour = int(input('Enter rate per hour  : '))

    dedcution = Deductions(u_dedcutionid,u_decname,u_rate,u_payrollno,u_employeeid,u_hours,u_rateperhour)    


    new_dedecution = {
        'dedcution_id' : dedcution.id,
        'dedcution_name': dedcution.deduction_name,
        'deduction_rate':dedcution.deduction_rate,
        'Payroll number ' : dedcution.payrollnumber,
        'Employee_id' : dedcution.employeeid,
        'Salary ':dedcution.get_salary(),
        'Amount to be paid' : dedcution.compute_amount(),
        
    }

    
        

    with open ("deduction.json",'w') as file :
            dedcutions.append(new_dedecution)
            json.dump( dedcutions,file, indent = 4)
    


   
    add_depat = input ('Do you want to add another deduction (y/n) :')    

    if  add_depat == 'y' :
        continue 
    else :
        break 