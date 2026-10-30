
# need to make the rate automatic 

from oop_prac import Deductions
from storage import DuplicateRecordError, StorageError, append_record


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
        'deduction_id': deduction.id,
        'name': deduction.deduction_name,
        'rate': deduction.deduction_rate,
        'payroll_id': deduction.payrollnumber,
        'employee_id': deduction.employeeid,
        'salary': deduction.salary,
        'amount': deduction.compute_amount(),
    }
    try:
        append_record('deductions', new_dedecution, 'deduction_id')
        print('Record saved successfully')
    except (DuplicateRecordError, StorageError) as error:
        print(error)
    
   
    add_depat = input ('Do you want to add another deduction (y/n) :')    

    if  add_depat == 'y' :
        continue 
    else :
        break
