#id,employeename,totaldeductions,totalallowances,gross,hoursworked

from oop_prac import Payslip
import json
try:
    with open ('payslip.json','r') as file :
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
    print(payslip)
    payslip.set_gross(salary) 
    payslip.compute_net()
    

    new_payslip = {
        'Payslip id' : payslip.id,
        'Total deductions  ' : payslip.totaldeductions,
        'Total allowances ' : payslip.totalallowances,
        'hours worked' : payslip.hoursworked,
        'gross' :payslip.get_gross (),
        'net' : payslip.get_net(),
        
    }
    
 
    with open ("payslip.json",'w') as file :
                payslips.append(new_payslip)
                json.dump( new_payslip,file, indent = 4)
    
            
    add_payslip = input ('Do you want to add another payslip (y/n) : ')    
    
    if  add_payslip == 'y' :
            continue 
    else :
            break 