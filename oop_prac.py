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



class Deductions:
        def __init__(self,ID,Deductionname,Deductionrate,Payrollnumber,Amount,EmployeeID):
            self.ID =ID
            self.Deduction_name =Deductionname
            self.Deduction_rate =Deductionrate
            self.Payrollnumber =Payrollnumber
            self.Amount =Amount
            self.EmployeeID =EmployeeID

        def calculated(self):
            pass

        def complaint(self):
            pass


class Allowance:
    def __init__(self,ID,PayrollID,EmploymentID,Name,Rate):
        self.ID =ID
        self.PayrollID =PayrollID
        self.EmploymentID =EmploymentID
        self.Name =Name
        self.Rate =Rate

    def fixed(self):
        pass

    def specific(self):
        pass



class Payroll:
    def __init__(self,ID,Year,Date,Month):
        self.ID =ID
        self.Year =Year
        self.Date =Date
        self.Month =Month

    def generated(self):
        pass

    def reported(self):
        pass

    def calculated(self):
        pass



class Payslip:
    def __init__(self,ID,Employeename,Totaldeductions,Totalallowances,Gross,Net,Hoursworked):
        self.ID =ID
        self.Employeename =Employeename
        self.Totaldeductions =Totaldeductions
        self.Totalallowances =Totalallowances
        self.Gross =Gross
        self.Net =Net
        self.Hoursworked =Hoursworked

    def issues(self):
        pass

    def personalised(self):
        pass

    def summarised(self):
        pass
        
        
    


    
            