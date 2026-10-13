from oop_prac import Allowance,Deductions,Salary,Payroll,Payslip,Position,Employee

print ("\tOPTIONS1.ALLOWANCE\n2.DEDUCTIONS\n3.SALARY\n4.PAYROLL\n5.PAYSLIP\n6.POSITION\n7.EMPLOYEE\n8.DEPARTMENT")


option = input('Enter Option : ')
if option == '1':
    import json


    try:
        with open ('allowance.json','r') as file :
            allowances= json.load(file)

            print(type(allowances))
            print(allowances)


    except FileNotFoundError:
        print("File not found. Creating a new file.")
        allowances= []

    except json.decoder.JSONDecodeError:
        print('File not yet created. Creating a new file')
        allowances = []
        

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
            'Allowance id' : allowance.id,
            'Payroll number  ' :  allowance.payrollid,
            'Employment id ' : allowance.employmentid,
            'Allowance name ' : allowance.name,
            'Allowance rate ' : allowance.rate,
            
        }

        allowances.append(new_allowance)
            
    
        with open ("allowance.json",'w') as file :
                json.dump(allowances,file, indent = 4)




            
        add_allowance = input ('Do you want to add another allowance (y/n) : ')    

        if  add_allowance == 'y' :
            continue 
        else :
            break 

elif option == '2'  :
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

elif option =='3':
    import json 
    try:
        with open ('salary.json','r') as file :
                salaries = json.load(file)


    except FileNotFoundError:
        print("File not found. Creating a new file.")
        salaries = []

    while True:
        u_employee_id = input ('Enter employee id : ')
        u_hoursworked = int(input ('Enter hoursworked :'))
        u_rate =int( input ('Enter rate :'))

        salary = Salary(u_employee_id,u_hoursworked,u_rate)
        paidsalary = salary.get_salary()
        print(f'SALARY : {paidsalary}')

        new_dedecution = {
                'Employee_id' : salary.employee_id,
                'hours_worked': salary.hoursworked,
                'Hour_rate':salary.rateperhour,
                'Salary ' : salary.get_salary(),
                
            }
        with open ("salary.json",'w') as file :
                    salaries.append(new_dedecution)
                    json.dump(salaries,file, indent = 4)
            
        
        add_salary = input ('Do you want to add another employees salary  (y/n) :')    

        if  add_salary == 'y' :
                continue 
        else :
                break  

elif option == '4' :           

    import json 

    try:
        with open ('payroll.json','r') as file :
         payrolls = json.load(file)


    except FileNotFoundError:
        print("File not found. Creating a new file.")
        payrolls = []
        
    #datetime is not JSON serializable        
    while True:
        payroll_id = input ('Enter payroll_id  : ')

        payroll = Payroll(payroll_id)
        print(payroll)

        new_payroll = {
                    'Payslip id' : payroll.payrollid,
                    'Date'  : payroll.caculate_date().isoformat()
                }
            
        payrolls.append(new_payroll)
            
        with open ("payslips.json",'w') as file :
                    json.dump(new_payroll,file, indent = 2)
                
                        
        add_payslip = input ('Do you want to add another payslip (y/n) : ')    
                
        if  add_payslip == 'y' :
            continue 
        else :
            break

elif option == '5'   :
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
            'Employee name ' : payslip.employeename,
            'Total deductions  ' : payslip.totaldeductions,
            'Total allowances ' : payslip.totalallowances,
            'hours worked' : payslip.hoursworked,
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

elif option == '6'    :
    import json

    while True :
        u_title = input ("Enter title : ")
        u_department = input ("enter department : ") 
        u_salary =  input ('Enter salary ')

        position = Position(u_title,u_department,u_salary)
        
        print ('\t++++++POSITION DETAILS++++++')
        #print (position)

        new_position = {
                'Title' : position.title,
                'Department' :  position.department,
                'Salary' : position.salary,   
            }

        with open ('position.json','r') as file :
                positions = json.load(file) 
        
        positions.append(new_position)
        with open ('position.json','w') as file :
            json.dump(positions,file,indent=4)

        add_position = input ('Do you want to add another position (y/n) : ')    
        
        if  add_position == 'y' :
                continue 
        else :
                break  

elif option == '7'   :
    import json


    try:
        with open ('employee.json','r') as file :
                employees = json.load(file)
                print(type(employees))
                print(employees)
    

    except FileNotFoundError:
        print("File not found. Creating a new file.")
        employees= []

    except json.decoder.JSONDecodeError:
        print('File not yet created. Creating a new file')
        employees = []
    

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
            'employeeid' : employee.id,
            'First name ' :  employee.firstname,
            'Last name ' : employee.lastname,
            'Birth year' : employee.dateofbirth,
            'Department' : employee.department,
            'Gender' : employee.gender,
            'Status' : employee.status,
            'Position' : employee.position,
            'Contact' : employee.contact,
            'Address' : employee.get_address(),
            'Age'     :employee.get_age(),
            
        }

        
            

        with open ("employee.json",'w') as file :
                employees.append(new_employee)
                json.dump( employees,file, indent = 4)

            
        add_employee = input ('Do you want to add employee  (y/n) :')    

        if  add_employee == 'y' :
            continue 
        else :
            break                                                           