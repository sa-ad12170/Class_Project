from oop_prac import Allowance,Deductions,Salary,Payroll,Payslip,Position,Employee
from storage import DuplicateRecordError, StorageError, append_record


def save_record(collection, record, unique_fields):
    try:
        append_record(collection, record, unique_fields)
        print('Record saved successfully')
        return True
    except (DuplicateRecordError, StorageError) as error:
        print(error)
        return False

print("\tOPTIONS\n1.ALLOWANCE\n2.DEDUCTIONS\n3.SALARY\n4.PAYROLL\n5.PAYSLIP\n6.POSITION\n7.EMPLOYEE\n8.DEPARTMENT")


option = input('Enter Option : ')
if option == '1':
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
        save_record('allowances', new_allowance, 'allowance_id')
            
        add_allowance = input ('Do you want to add another allowance (y/n) : ')    

        if  add_allowance == 'y' :
            continue 
        else :
            break 

elif option == '2'  :
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
        save_record('deductions', new_dedecution, 'deduction_id')
        
    
        add_depat = input ('Do you want to add another deduction (y/n) :')    

        if  add_depat == 'y' :
            continue 
        else :
            break          

elif option =='3':
    while True:
        u_employee_id = input ('Enter employee id : ')
        u_hoursworked = int(input ('Enter hoursworked :'))
        u_rate =int( input ('Enter rate :'))

        salary = Salary(u_employee_id,u_hoursworked,u_rate)
        paidsalary = salary.get_salary()
        print(f'SALARY : {paidsalary}')

        new_salary = {
            'employee_id': salary.employee_id,
            'hours_worked': salary.hoursworked,
            'rate_per_hour': salary.rateperhour,
            'salary': salary.get_salary(),
        }
        save_record('salaries', new_salary, 'employee_id')
            
        
        add_salary = input ('Do you want to add another employees salary  (y/n) :')    

        if  add_salary == 'y' :
                continue 
        else :
                break  

elif option == '4' :           
    while True:
        payroll_id = input ('Enter payroll_id  : ')

        payroll = Payroll(payroll_id)
        print(payroll)

        new_payroll = {
            'payroll_id': payroll.payrollid,
            'issued_at': payroll.date.isoformat(),
        }
        save_record('payrolls', new_payroll, 'payroll_id')
                
                        
        add_payslip = input ('Do you want to add another payslip (y/n) : ')    
                
        if  add_payslip == 'y' :
            continue 
        else :
            break

elif option == '5'   :
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
            'payslip_id': payslip.id,
            'employee_name': payslip.employeename,
            'total_deductions': payslip.totaldeductions,
            'total_allowances': payslip.totalallowances,
            'hours_worked': payslip.hours_worked,
            'gross': payslip.get_gross(),
            'net': payslip.get_net(),
        }
        save_record('payslips', new_payslip, 'payslip_id')
        
                
        add_payslip = input ('Do you want to add another payslip (y/n) : ')    
        
        if  add_payslip == 'y' :
                continue 
        else :
                break   

elif option == '6'    :
    while True :
        u_title = input ("Enter title : ")
        u_department = input ("enter department : ") 
        u_salary =  input ('Enter salary ')

        position = Position(u_title,u_department,u_salary)
        
        print ('\t++++++POSITION DETAILS++++++')
        #print (position)

        new_position = {
            'title': position.title,
            'department': position.department,
            'salary': position.salary,
            'status': position.status(),
        }
        save_record('positions', new_position, ('title', 'department'))

        add_position = input ('Do you want to add another position (y/n) : ')    
        
        if  add_position == 'y' :
                continue 
        else :
                break  

elif option == '7'   :
    while True :
    #user input    
        u_employeeid = input ('Enter employee id : ')
        u_fname = input ('Enter first name  : ')
        u_last = input ('Enter last name   : ')
        u_dateofbirth = int(input('Enter birth year : '))
        u_department = input('Enter department : ')
        u_gender = input('Enter gender : ')
        u_status = input('Enter status : ')
        u_contact = input('Enter contact : ')
        u_position = input('Enter position : ')
        u_village = input('Enter village: ')
        u_city = input('Enter city : ')
        
        
        
        

        employee = Employee(u_employeeid,u_fname,u_last ,u_dateofbirth,u_department,u_gender ,u_status,u_contact ,u_village,u_city,u_position) 
        


        new_employee = {
            'employee_id': employee.id,
            'first_name': employee.firstname,
            'last_name': employee.lastname,
            'birth_year': employee.dateofbirth,
            'department': employee.department,
            'gender': employee.gender,
            'status': employee.status,
            'position': employee.position,
            'contact': employee.contact,
            'address': employee.get_address(),
            'age': employee.get_age(),
        }
        save_record('employees', new_employee, 'employee_id')

            
        add_employee = input ('Do you want to add employee  (y/n) :')    

        if  add_employee == 'y' :
            continue 
        else :
            break

elif option == '8':
    from department import run_department_menu

    run_department_menu()

else:
    print('Invalid option')
