class Department:
    def __init__(self,deptid,name,number_of_staff):
       self.deptid = deptid
       self.name =name
       self.number_of_staff = number_of_staff

    def add(self):
        pass

    def count(self):
        pass

    def remove(self):
        pass

    def display(self):
        pass

#child class from employee parent class 
class Position:
    def __init__(self,title,department,name,salary):
        self.title =title
        self.department =department
        self.name =name
        self.salary =salary

    def  roles(self):
        pass
    
    def assigned(self):
        pass

    def status(self):
        pass



class Employee:
    def __init__(self,id,firstname,lastname,dateofbirth,department,gender,status,contact,village,city):
        self.id =id
        self.firstname =firstname
        self.lastname =lastname
        self.dateofbirth =dateofbirth
        self.department =department
        self.contact = contact
        self.village = village 
        self.city = city
        self.__address = self.set_address()
        self.gender =gender
        self.status =status
        self.position = None 
        self.__age = self.compute_age()
        self.salary = 0
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

    def hired(self):
        pass

    def fired(self):
        pass

    def promoted(self):
        pass
# make a childclass salary from employee

#child class of employee 
class Deductions:
        def __init__(self,id,deductionname,deductionrate,payrollnumber,employeeid,hoursworked,rateperhour):
            self.id =id
            self.deduction_name =deductionname
            self.deduction_rate =deductionrate
            self.payrollnumber =payrollnumber
            self.employeeid =employeeid
            self.hoursworked = hoursworked 
            self.rateperhour = rateperhour
            self.__salary = self.set_salary()
            self.__amount = self.compute_amount()

        def set_salary (self):
            self.__salary = self.hoursworked  * self.rateperhour  
            return self.__salary
        def get_salary (self):
            return self.__salary 
#different rates for different deductions
        def compute_amount(self):
            self.__amount =  (self.__salary * (self.deduction_rate/100 ))
            return self.__amount
        def get_amount (self):
            return self.__amount


class Allowance:
    def __init__(self,id,payrollid,employmentid,name,rate):
        self.id =id
        self.payrollid =payrollid
        self.employmentid =employmentid
        self.name =name
        self.rate =rate

    def fixed(self):
        pass

    def specific(self):
        pass



class Payroll:
    def __init__(self,issuer):
     self.issuer = issuer 
     self.date = self.caculate_date()
    def caculate_date (self) :
     from datetime import datetime
     self.date = datetime.now()
     return self.date 
    def __str__(self):
        return f'Payroll has been issused by {self.issuer} on {self.date}'
    #NEED TO GET A LIST OF ALL EMPLOYESS PAID AND THEIR RESPECTIVE SALARIES SO THAT WE CAN GET THE TOTAL OF THE PAYROLL 

    


#child class from employeeS
class Payslip:
    def __init__(self,id,employeename,totaldeductions,totalallowances,gross,hoursworked):
        self.id =id
        self.employeename =employeename
        self.__totaldeductions =totaldeductions
        self.__totalallowances =totalallowances
        self.__gross = gross
        self.__net = self.compute_net()
        self.__hoursworked =hoursworked

    

    def setgross(self)  :
        self.__gross = self.__totalallowances #we nedd ythe salary from the parent class 



    def compute_net(self):
        self.__net = self.__gross - self.__totaldeductions
        return self.__net 
    def get_net(self):
        return self.__net

    
        
        
    


    
            