#id,employeename,totaldeductions,totalallowances,gross,hoursworked

from oop_prac import Payslip
import json
try:
    with open ('payslips.json','r') as file :
     payslips = json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    payslips = []
   
while True :
    u_payslipid = input ('Enter Payslip id : ')
    u_employeename = input ('Enter employee name : ')
    u_totaldeductions = int(input ('Enter  totaldeductions : '))
    u_totalallowances= int(input ('Enter totalallowances  : '))
    u_hoursworked = int(input ('Enter hoursworked : '))
    salary = int(input('Enter salary : '))

    payslip = Payslip (u_payslipid,u_employeename,u_totaldeductions,u_totalallowances,u_hoursworked)

    payslip.set_gross(salary)
    #print(payslip)
     
    payslip.compute_net()

    payslip.Payments()
    

    new_payslip = {
        'Payslip id' : payslip.id,
        'Employee name ' : payslip.employeename,
        'Total deductions  ' : payslip.totaldeductions,
        'Total allowances ' : payslip.totalallowances,
        'hours worked' : payslip.hours_worked,
        'Gross' : payslip.get_gross (),
        'Net' : payslip.get_net(),
        
    }
    payslips.append(new_payslip)
 
    with open ("payslips.json",'w') as file :
        
        json.dump( payslips,file, indent = 4)
    
            
    add_payslip = input ('Do you want to add another payslip (y/n) : ')    
    
    if  add_payslip == 'y' :
            continue 
    else :
            break 