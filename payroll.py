from oop_prac import Payroll
import json 
'''
try:
    with open ('payroll.json','r') as file :
     payrolls = json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    payrolls = []
'''    
#datetime is not JSON serializable        

payroll_id = input ('Enter payroll_id  : ')

payroll = Payroll(payroll_id)
print(payroll)
'''
    new_payroll = {
            'Payslip id' : payroll.payrollid,
            'Date'  : payroll.caculate_date()
        }
    
    payrolls.append(new_payroll)
    
    with open ("payslips.json",'w') as file :
            
            json.dump(new_payroll,file, indent = 2)
        
                
    add_payslip = input ('Do you want to add another payslip (y/n) : ')    
        
    if  add_payslip == 'y' :
                continue 
    else :
                break
'''                 