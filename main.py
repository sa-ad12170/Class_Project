from oop_prac import Allowance,Deduction,Salary,Payroll,Payslip,Position,Employee,Department 
import json
#print ("\tOPTIONS1.ALLOWANCE\n2.DEDUCTIONS\n3.SALARY\n4.PAYROLL\n5.PAYSLIP\n6.POSITION\n7.EMPLOYEE\n8.DEPARTMENT")

#EMPLOYEE  
try:
        with open ('main.json','r') as file :
                mainjson = json.load(file)
                #print(type(mainjson))
                print(mainjson)
    

except FileNotFoundError:
        print("File not found. Creating a new file.")
        mainjson= []

except json.decoder.JSONDecodeError:
        print('File not yet created. Creating a new file')
        mainjson= []
    

#while True :
    #user input    
u_employeeid = Employee.generate_id () 
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





employee = Employee(u_fname,u_last ,u_dateofbirth,u_department,u_gender ,u_status,u_contact ,u_village,u_city,u_position) 



new_employee = {
        'employeeid' : employee.empid,
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


        

with open ("main.json",'w') as file :
        mainjson.append(new_employee)
        json.dump( mainjson,file, indent = 4)

#DEPARTMENT 

try:
        with open ('main.json','r') as file :
            mainjson= json.load(file)

            


except FileNotFoundError:
        print("File not found. Creating a new file.")
        mainjson= []

except json.decoder.JSONDecodeError:
        print('File not yet created. Creating a new file')
        mainjson = []
        

while True :
    #user input    
        u_id = Department.generate_id ()
        dept_name =input('Enter deptartment name : ')
        
        department  = Department(dept_name)
        print(department)

        
        

        new_department  = {
            'Department id' : department.deptid,
            'Department name  ' : department.departmentname
            
            
        }

        mainjson.append(new_department)
        department.add_staff(employee) 
        department.display_staff()
        

        with open ("main.json",'w') as file :
                json.dump(mainjson,file, indent = 4)


         
        add_department = input ('Do you want to add another department (y/n) : ')    

        if  add_department  == 'y' :
            continue 
        else :
            break         

            
       
#SALARY 
try:
        with open ('main.json','r') as file :
                mainjson= json.load(file)


except FileNotFoundError:
        print("File not found. Creating a new file.")
        mainjson = []


u_hoursworked = int(input ('Enter hoursworked : '))
u_rate =int( input ('Enter rate :'))

salary = Salary(employee.empid,employee.firstname,u_hoursworked,u_rate) # employee composition 
paidsalary = salary.get_salary()
print(f'SALARY : {paidsalary}')

new_employee = {
        'Employee_id' : salary.employee_id,
        "Employee name  ":salary.employeename,
        'hours_worked': salary.hoursworked,
        'Hour_rate':salary.rateperhour,
        'Salary ' : salary.get_salary(),
        
    }
with open ("main.json",'w') as file :
            mainjson.append(new_employee)
            json.dump(mainjson,file, indent = 4)
           
##PAYROLL     

try:
        with open ('payroll.json','r') as file :
         payrolls = json.load(file)


except FileNotFoundError:
        print("File not found. Creating a new file.")
        payrolls = []
        
  
payroll_id = Payroll.generate_id() 

payroll = Payroll()
print(payroll)

new_payroll = {
                'Payslip id' : payroll.payrollid,
                'Date'  : payroll.caculate_date().isoformat()
        }
        
payrolls.append(new_payroll)
        
with open ("payslips.json",'w') as file :
                json.dump(new_payroll,file, indent = 2)
        
                                       
       
#ALLOWANCE 

try:
        with open ('main.json','r') as file :
            mainjson= json.load(file)
           
except FileNotFoundError:
        print("File not found. Creating a new file.")
        mainjson= []

except json.decoder.JSONDecodeError:
        print('File not yet created. Creating a new file')
        mainjson = []

while True :       
       
        
        u_id = Allowance.generate_id ()
        u_name =input('Enter  allowance name : ')
        u_rate =int(input('Enter allowance rate : '))
        allowance  = Allowance(payroll.payrollid,employee.empid ,u_name,u_rate,salary.salaryamount) # implemented composition 
        
 
     
        new_allowance = {
        'Allowance id' : allowance.id,
        'Payroll number  ' :  allowance.payrollid,
        'Employment id ' : allowance.employmentid,
        'Allowance name ' : allowance.name,
        'Allowance rate ' : allowance.rate,
        'Allowance amount' :allowance.compute_amount(),
       
       }

        mainjson.append(new_allowance)
        allowance_list  = allowance.add_allowance(allowance.amount)
        
 
        with open ("main.json",'w') as file :
                json.dump(mainjson,file, indent = 4)

                

        add_allowance = input ('Do you want to add another allowance (y/n) : ')    
        
        if  add_allowance  == 'y' :
                continue 
        else :
                break   
print (allowance_list)             

#DEDUCTION         
try:
        with open ('main.json','r') as file :
                mainjson = json.load(file)


except FileNotFoundError:
        print("File not found. Creating a new file.")
        mainjson= []
except json.decoder.JSONDecodeError:
        print('File not yet created. Creating a new file')
        mainjson = []        


u_deductionid = Deduction.generate_id
u_decname = input ('Enter decution name  :')
u_rate = int(input ('Enter rate of deduction  :'))



deduction = Deduction(u_decname,u_rate,payroll.payrollid,employee.empid,salary.salaryamount)    

new_dedecution = {
        'deduction_id' : deduction.id,
        'deduction_name': deduction.deduction_name,
        'deduction_rate':deduction.deduction_rate,
        'Payroll number ' : deduction.payrollnumber,
        'Employee_id' : deduction.employeeid,
        'salary' : deduction.salary,
        'Amount to be deducted' : deduction.compute_amount(),
        
} 

with open ("main.json",'w') as file :
                mainjson.append(new_dedecution)
                json.dump( mainjson,file, indent = 4)
        
       
#PAYSLIP              
try:
        with open ('main.json','r') as file :
         mainjson = json.load(file)

except FileNotFoundError:
        print("File not found. Creating a new file.")
        mainjson = []
    

u_payslipid =  Payslip.generate_id() 

payslip = Payslip (employee.firstname,deduction.amount,allowance.amount,salary.hoursworked)#applied composition
print(payslip)
payslip.set_gross(salary.salaryamount) 
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
mainjson.append(new_payslip)

with open ("mainjson.json",'w') as file :
    
        json.dump( mainjson,file, indent = 4)
    
        
#NEDD TO MOVE POSITIOON OBJECT        
#title \position 
   
u_title = employee.position
u_department = department.departmentname 
u_salary =  salary.salaryamount


position = Position(u_title,u_department,u_salary)

print ('\t++++++POSITION DETAILS++++++')
print (position)

