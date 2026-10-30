from abc import ABC , abstractmethod
class Department:
    def __init__(self,deptid,name):
       self.deptid = deptid
       self.departmentname =name
       self.staff = []

    def add_staff(self,employee):
        self.staff.append (employee)
        return self.staff

    def remove_staff(self,employee_id):
        for employee in self.staff:
            if employee['id'] == employee_id:
                self.staff.remove(employee)
                return 'Staff member has been removed'
        return 'Staff member not found'

    def display_staff(self):
        print (f'Staff in {self.departmentname}:')
        if len(self.staff) == 0 :
            print ('No staff in this department ')
        for employee in self.staff :
            print(f"ID : {employee['id']}\nName : {employee['name']}\nPosition:{employee['position']}")

    def get_no_of_staff(self)  :
        return len(self.staff) 
    #converting the class into  a json 
    def to_dict (self )    :
        return {
            'Department id':self.deptid,
            'Department name':self.departmentname,
            'Department staff':self.staff,
        } 


#child class from employee parent class 
class Position:
    def __init__(self,title,department,salary):
        self.title =title
        self.department =department#composition
        self.salary =salary#composition to salary scale

    def __str__(self):
        return f'Title : {self.title}\nDepartment :{self.department}\nSalary : {self.salary}'    

    def status(self):
            pass#result should be vacant or occupied
    

   



class Employee:
    employee = 0



    def __init__(self,id,firstname,lastname,dateofbirth,department,gender,status,contact,village,city,position):
        self.id =id
        self.firstname =firstname
        self.lastname =lastname
        self.dateofbirth =dateofbirth
        self.department =department#composition
        self.contact = contact
        self.village = village 
        self.city = city
        self.__address = self.set_address()#irrelevant
        self.gender =gender
        self.status =status#fired or active
        self.position = position.upper()#issue(should  not be none) and composition
        self.__age = self.compute_age()
        self.__salary = 0 #composition
       #need to make method for position
       # 
    @classmethod
    def generate_id(cls):
        al = "Emp"
        cls.employee +=1 
        return al + str(cls.employee) 

    



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
    #add an abstrsctmethod 
    def compute_salary (self):
        return self.__salary     
        
class SalaryScale:
    def __init__(self,employeeid,position):
        self.employeeid = employeeid#to be composed
        self.position = position#to be composed
        self.salary = 0

        if self.position == "regular".lower().strip():
            self.salary = 500000

        elif self.position == "team_leader".lower().strip():
            self.salary = 7000000

        elif self.position == "department_head".lower().strip():
            self.salary = 900000

        elif self.position == "ceo".lower().strip():
            self.salary = 2000000

        elif self.position == "coo".lower().strip():
                self.salary = 40000000

        else:
            print('position not available')


class Deductions:
        def __init__(self,id,deductionname,deductionrate,payrollnumber,employeeid,salary):
            self.id =id
            self.deduction_name =deductionname
            self.deduction_rate =deductionrate
            self.payrollnumber =payrollnumber
            self.employeeid =employeeid#compose
            self.salary = salary#compose
            self.__amount = self.compute_amount()

        
#different rates for different deductions
        def compute_amount(self):
            self.__amount =  (self.salary * (self.deduction_rate/100 ))
            return self.__amount
        def get_amount (self):
            return self.__amount


class Allowance:
    def __init__(self,id,payrollid,employmentid,name,rate):
        self.id =id
        self.payrollid =payrollid
        self.employmentid =employmentid#composition
        self.name =name
        self.rate =rate

    def __str__(self):
        return f'Payroll id :{self.payrollid}\nAllowance Id :{self.id}\nEmployee Id :{self.employmentid}\nAllowance Rate :{self.name}\nRate :{self.rate}'




class Payroll:
    def __init__(self,payrollid):
     self.payrollid = payrollid 
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

class Pay(ABC):
    
    @abstractmethod
    def Payments(self):
        pass
#above is what i have introduced

class Payslip(Pay):
    def __init__(self,id,employeename,totaldeductions,totalallowances,hours_worked):
        self.id =id
        self.employeename =employeename
        self.totaldeductions =totaldeductions#compose from allowances
        self.totalallowances =totalallowances#compose from allowances
        self.hours_worked = hours_worked
        self.__gross = 0 
        self.__net = self.compute_net()
        

    # def __str__(self):
    #     return f'Payslip id -------->\t{self.id}\nTotal Deductions\t: {self.totaldeductions}\nTotal Allowances\t: {self.totalallowances}\nHours Worked\t: {self.hours_worked}'

    def set_gross(self,salary)  :
        self.__gross = salary  + self.totalallowances
        return self.__gross
        
    def get_gross (self):
        return self.__gross 


    def compute_net(self):
        self.__net = self.get_gross() - self.totaldeductions
        return self.__net 
    
    def get_net(self):
        return self.__net

    def Payments(self):
        print(f"Payment details for {self.employeename}")
        print(f"Net salary: {self.get_net()}")


        
        
    


    
            