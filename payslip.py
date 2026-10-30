#id,employeename,totaldeductions,totalallowances,gross,hoursworked

from oop_prac import Payslip
from storage import DuplicateRecordError, StorageError, append_record
   
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
        'payslip_id': payslip.id,
        'employee_name': payslip.employeename,
        'total_deductions': payslip.totaldeductions,
        'total_allowances': payslip.totalallowances,
        'hours_worked': payslip.hours_worked,
        'gross': payslip.get_gross(),
        'net': payslip.get_net(),
    }
    try:
        append_record('payslips', new_payslip, 'payslip_id')
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)
    
            
    add_payslip = input ('Do you want to add another payslip (y/n) : ')    
    
    if  add_payslip == 'y' :
            continue 
    else :
            break
