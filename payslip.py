#id,employeename,totaldeductions,totalallowances,gross,hoursworked

from oop_prac import Payslip

u_payslipid = input ('Enter Payslip id : ')
u_employeename = input ('Enter employee name : ')
u_totaldeductions = int(input ('Enter  totaldeductions : '))
u_totalallowances= int(input ('Enter totalallowances  : '))
u_hoursworked = int(input ('Enter hoursworked : '))

payslip = Payslip (u_payslipid,u_employeename,u_totaldeductions,u_totalallowances,u_hoursworked)

print(payslip)
payslip.setgross(1000000)
gross = payslip.get_gross ()
net = payslip.get_net()
print(f'Total Gross : {gross}\nTotal net : {net}')