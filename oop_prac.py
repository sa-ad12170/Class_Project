class Department:
    def _init_(self,DeptID,Name,Number_of_staff):
       self.DeptID = DeptID
       self.Name =Name
       self. Number_of_staff =Number_of_staff

    def add(self):
        pass

    def count(self):
        pass

    def remove(self):
        pass

    def display(self):
        pass


class Position:
    def __init__(self,Title,Department,Name,Salary):
        self.Title =Title
        self.Department =Department
        self.Name =Name
        self.Salary =Salary

    def  roles(self):
        pass
    
    def assigned(self):
        pass

    def terminated(self):
        pass



class Employee:
    def __init__(self,ID,Firstname,Lastname,Dateofbirth,Department,Contact,Address,Gender,Status):
        self.ID =ID
        self.Firstname =Firstname
        self.Lastname =Lastname
        self.Dateofbirth =Dateofbirth
        self.Department =Department
        self.Contact =Contact
        self.Address =Address
        self.Gender =Gender
        self.Status =Status

    def paid(self):
        pass

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
        
        
    


    
            