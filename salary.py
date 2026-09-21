from oop_prac import Salary

u_employee_id = input ('Enter employee id :')
u_hoursworked = int(input ('Enter hoursworked :'))
u_rate =int( input ('Enter rate :'))

salary = Salary(u_employee_id,u_hoursworked,u_rate)
paidsalary = salary.get_salary()
print(f'SALARY : {paidsalary}')