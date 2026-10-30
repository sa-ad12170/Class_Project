from oop_prac import Allowance
from storage import DuplicateRecordError, StorageError, append_record
    

while True :
#user input    
    u_id = input('Enter allowance id : ')
    u_payrollid =input('Enter payrollid : ')
    u_employmentid =input('Enter employmentid : ')
    u_name =input('Enter  allowance name : ')
    u_rate =input('Enter allowance rate : ')

    allowance  = Allowance(u_id,u_payrollid,u_employmentid,u_name,u_rate)
    print(allowance)

    
    

    new_allowance = {
        'allowance_id': allowance.id,
        'payroll_id': allowance.payrollid,
        'employee_id': allowance.employmentid,
        'name': allowance.name,
        'rate': allowance.rate,
    }
    try:
        append_record('allowances', new_allowance, 'allowance_id')
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)




        
    add_allowance = input ('Do you want to add another allowance (y/n) : ')    

    if  add_allowance == 'y' :
        continue 
    else :
        break
