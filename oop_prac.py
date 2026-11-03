class Employee:
    emp = 0 
    @classmethod
    def generate_id(cls):
        d_id = "EMP"
        cls.emp +=1 
        return d_id + str(cls.emp)
    
    def __init__(self,firstname,lastname,dateofbirth,department,gender,status,contact,village,city,position):
        self.empid = self.generate_id()
        self.firstname =firstname
        self.lastname =lastname
        self.dateofbirth =dateofbirth
        self.department =department
        self.contact = contact
        self.village = village 
        self.city = city
        self.__address = self.set_address()#irrelevant
        self.gender =gender
        self.status =status
        self.position = position#issue(should  not be none)
        self.__age = self.compute_age()
        self.__salary = 0
       #need to make method for position 

    def set_address (self):
        self.__address = f'{self.village.upper()} in {self.city.upper()}'
        return self.__address
    
    def get_address (self):
        return self.__address

#automatically used to compute age 
    def compute_age(self):
        from datetime import datetime
        currentyear = datetime.today().year
        self.__age = currentyear - int(self.dateofbirth)
        return self.__age 
    def get_age (self):
        return self.__age



class Department:
    deptid = 0
    @classmethod
    def generate_id(cls):
        d_id = "Dept"
        cls.deptid +=1 
        return d_id + str(cls.deptid)
    
    def __init__(self,name):
       self.deptid = self.generate_id() 
       self.departmentname =name
       self.staff = []

    def add_staff(self,employee):
        self.staff.append (employee)
        #return self.staff

    def remove_staff(self,employee_id):
        for employee in self.staff:
            if employee['id'] == employee_id:
                self.staff.remove(employee)
                return 'Staff member has been removed'
        return 'Staff member not found'

    def display_staff(self):#composition
        output = ""
        for employee in self.staff:
            output += f"-->{employee}\n"
            return output 

        #print (f'Staff in {self.departmentname}:')
         #if len(self.staff) == 0 :
          #   print ('No staff in this department ')
         #for employee in self.staff :
             #print(f"ID : {employee['id']}\nName : {employee['name']}\nPosition:{employee['position']}")

    def get_no_of_staff(self)  :
        return len(self.staff) 
    #converting the class into  a json 
    def to_dict (self )    :
        return {
            'Department id':self.deptid,
            'Department name':self.departmentname,
            'Department staff':self.staff,
        } 
    def __str__(self):
        return f'DEPARTMENT : {self.departmentname} '    


#child class from employee parent class 
class Position:
    def __init__(self,title,department,salary):
        self.title =title
        self.department =department
        self.salary =salary

    def __str__(self):
        return f'Title : {self.title}\nDepartment :{self.department}\nSalary : {self.salary}'    

    def  roles(self):
        pass
    
    def assigned(self):
        pass

    def status(self):
        pass





'''
make a method status thatt combines the hired fired active and promoted 
'''
    # make a childclass salary from employee
class Salary : 
    def __init__(self,employee_id,employeename,hoursworked,rateperhour):
        self.employee_id = employee_id# apply composition
        self.employeename = employeename
        self.hoursworked = hoursworked 
        self.rateperhour = rateperhour
        self.salaryamount = self.set_salary()# changed salary from private to public 

    def set_salary (self):
        self.__salary = self.hoursworked  * self.rateperhour  
        return self.__salary
    
    def get_salary (self):
        return self.__salary     
        
#child class of employee 
class Deduction:
        deduction_id= 0
        @classmethod
        def generate_id(cls):
            d_id = "Ded"
            cls.deduction_id +=1 
            return d_id + str(cls.deduction_id)
        def __init__(self,deductionname,deductionrate,payrollnumber,employeeid ,salary):
            self.id =self.generate_id()
            self.deduction_name =deductionname
            self.deduction_rate =deductionrate
            self.payrollnumber =payrollnumber
            self.employeeid =employeeid
            self.salary = salary
            self.amount = self.compute_amount()#made it public 

        
#different rates for different deductions
        def compute_amount(self):
            self.__amount =  (self.salary * (self.deduction_rate/100 ))
            return self.__amount
        def get_amount (self):
            return self.__amount


class Allowance:
    all_id= 0
    @classmethod
    def generate_id(cls):
        a_id = "ALl"
        cls.all_id +=1 
        return a_id + str(cls.all_id)
    def __init__(self,payrollid,employmentid,name,rate,salary):
        self.id =self.generate_id()
        self.payrollid =payrollid
        self.employmentid =employmentid
        self.name = name
        self.rate = rate
        self.salary = salary
        self.amount = self.compute_amount()

    def __str__(self):
        return f'Payroll id :{self.payrollid}\nAllowance Id :{self.id}\nEmployee Id :{self.employmentid}\nAllowance Rate :{self.name}\nRate :{self.rate}'
    def compute_amount(self):        
            self.amountrate = (self.rate/100)
            self.amount = self.amountrate * self.salary 
            return self.amount




class Payroll:
    pay_id= 0
    @classmethod
    def generate_id(cls):
        pa_id = "PAY"
        cls.pay_id +=1 
        return pa_id + str(cls.pay_id)
    def __init__(self):
     self.payrollid = self.generate_id()
     self.date = self.caculate_date()
     
    def caculate_date (self) :
     from datetime import datetime
     self.date = datetime.now()
     return self.date 
    
    def __str__(self):
        return f'Payroll with ID {self.payrollid} has been issued on {self.date}'
    #NEED TO GET A LIST OF ALL EMPLOYESS PAID AND THEIR RESPECTIVE SALARIES SO THAT WE CAN GET THE TOTAL OF THE PAYROLL 

    


#child class from employeeS
#has a bug 
class Payslip:
    pays_id= 0
    @classmethod
    def generate_id(cls):
        pa_id = "PAY"
        cls.pays_id +=1 
        return pa_id + str(cls.pays_id)
    
    def __init__(self,employeename,totaldeductions,totalallowances,hoursworked):
        self.id =self.generate_id()
        self.employeename =employeename
        self.totaldeductions =totaldeductions
        self.totalallowances =totalallowances
        self.hoursworked =hoursworked
        self.__gross = 0 
        self.__net = self.compute_net()
        

    def __str__(self):
        return f'Payslip id -------->\t{self.id}\nTotal Deductions\t: {self.totaldeductions}\nTotal Allowances\t: {self.totalallowances}\nHours Worked\t: {self.hoursworked}'

    def set_gross(self,salary)  :
        self.__gross = salary  + self.totalallowances
        return self.__gross
        
    def get_gross (self):
        return self.__gross 


    def compute_net(self):
        self.__net = self.__gross -  self.totaldeductions
        return self.__net 
    def get_net(self):
        return self.__net


        
        
    


    
            