from oop_prac import Allowance
import json


try:
    with open ('allowance.json','r') as file :
        allowances= json.load(file)


except FileNotFoundError:
    print("File not found. Creating a new file.")
    allowances= []

except json.JSONDecodeError:
    print("JSON file is empty or invalid. Starting with an empty list.")
    allowances = []
  

while True :
#user input    
    u_id = input('Enter allowance id : ')
    u_payrollid =input('Enter payrollid : ')
    u_employmentid =input('Enter employmentid : ')
    u_name =input('Enter  allowance name : ')
    u_rate =input('Enter allowance rate : ')

    allowance  = Allowance(u_id,u_payrollid,u_employmentid,u_name,u_rate)


    new_allowance = {
        'Allowance id' : allowance.id,
        'Payroll number  ' :  allowance.payrollid,
        'Employment id ' : allowance.employmentid,
        'Allowance name ' : allowance.name,
        'Allowance rate ' : allowance.rate,
        
    }

    
    allowances.append(new_allowance)  

    with open ("allowance.json",'w') as file :
            
            json.dump( allowances,file, indent = 4)

        
    add_allowance = input ('Do you want to add another allowance   (y/n) :')    

    if  add_allowance == 'y' :
        continue 
    else :
        break 