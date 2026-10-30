from oop_prac import Payroll
from storage import DuplicateRecordError, StorageError, append_record
    
#datetime is not JSON serializable        
while True:
    payroll_id = input ('Enter payroll_id  : ')

    payroll = Payroll(payroll_id)
    print(payroll)

    new_payroll = {
        'payroll_id': payroll.payrollid,
        'issued_at': payroll.date.isoformat(),
    }
    try:
        append_record('payrolls', new_payroll, 'payroll_id')
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)

    add_payslip = input ('Do you want to add another payslip (y/n) : ')    
            
    if  add_payslip == 'y' :
        continue 
    else :
        break
