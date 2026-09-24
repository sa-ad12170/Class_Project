
# need to make the rate automatic 

from oop_prac import Deductions
import json
#DeptID,Name,Number_of_staff

try:
    with open ('deduction.json','r') as file :
            dedcutions = json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    dedcutions = []


while True :
#user input    
    u_deductionid = input ('Enter deduction id :')
    u_decname = input ('Enter decution name  :')
    u_rate = int(input ('Enter rate of deduction  :'))
    u_payrollno = input ('Enter pay roll number  :')
    u_employeeid = input ('Enter employee id  :')
    u_salary = int(input('Enter employees salary : '))
    

    deduction = Deductions(u_deductionid,u_decname,u_rate,u_payrollno,u_employeeid,u_salary)    

    new_dedecution = {
        'deduction_id' : deduction.id,
        'deduction_name': deduction.deduction_name,
        'deduction_rate':deduction.deduction_rate,
        'Payroll number ' : deduction.payrollnumber,
        'Employee_id' : deduction.employeeid,
        'salary' : deduction.salary,
        'Amount to be deducted' : deduction.compute_amount(),
        
    } 

    with open ("deduction.json",'w') as file :
            dedcutions.append(new_dedecution)
            json.dump( dedcutions,file, indent = 4)
    
   
    add_depat = input ('Do you want to add another deduction (y/n) :')    

    if  add_depat == 'y' :
        continue 
    else :
        break 