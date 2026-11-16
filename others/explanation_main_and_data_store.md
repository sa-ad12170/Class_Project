# Explanation of `data_store.py` and `main.py`

This document explains how the current `data_store.py` and `main.py` files work. It does not change their code. Line numbers refer to the versions inspected when this document was created, so they may shift if the files are edited later.

## `data_store.py`

This file reads and writes the project's single JSON file, `data.json`.

### Imports and file settings (lines 1–6)

- **Line 1 — `import json`:** Imports Python's JSON tools. They convert JSON text into Python data and Python data back into JSON text.
- **Line 2 — `from pathlib import Path`:** Imports `Path`, a class for working with file paths.
- **Line 5 — `DATA_FILE = ...`:** Builds the path to `data.json`. `__file__` means this Python file; `.resolve()` gets its full path; `.parent` gets the folder containing it. The result points to `data.json` beside `data_store.py`.
- **Line 6 — `SECTIONS = (...)`:** Lists the allowed top-level sections in `data.json`. Each section is expected to be a list. Employee records are in the `departments` section, inside each department's `staff` list.

### `_load_data()` (lines 9–23)

This helper reads the whole JSON file and makes sure all expected sections are present.

- **Line 9:** Defines `_load_data`. The leading underscore is a Python naming convention that signals the function is mainly for internal use in this module.
- **Line 10:** The docstring briefly describes the function.
- **Line 11:** Starts a `try` block because opening or reading the JSON file can fail.
- **Line 12:** Opens `data.json` in read mode (`"r"`) using UTF-8 encoding. `with` closes the file automatically when the block ends.
- **Line 13:** `json.load(file)` reads the JSON text and converts it into Python values, usually dictionaries and lists.
- **Line 14:** Catches two problems: the file does not exist, or its contents are not valid JSON.
- **Line 15:** If either problem happens, starts with an empty dictionary.
- **Line 17:** Checks that the loaded top-level value is a dictionary.
- **Line 18:** If it is not a dictionary, replaces it with an empty dictionary.
- **Line 20:** Goes through each allowed section name in `SECTIONS`.
- **Line 21:** Checks whether that section currently contains a list.
- **Line 22:** If the section is missing or is not a list, sets it to an empty list.
- **Line 23:** Returns the dictionary with all expected sections available.

**Practical effect:** If the file is missing or contains invalid JSON, this function can create a usable in-memory structure. If a later save happens, that structure can be written to the file, replacing the invalid contents.

### `load_records(section)` (lines 26–30)

This function returns one section from `data.json`.

- **Line 26:** Defines the function. The caller supplies a section name, such as `"departments"` or `"payrolls"`.
- **Line 27:** Describes what the function returns.
- **Line 28:** Checks that the requested section is allowed.
- **Line 29:** Raises a `ValueError` if the caller asks for an unknown section. This helps catch misspelled section names.
- **Line 30:** Loads the JSON data and returns the list belonging to that section.

For example, `load_records("allowances")` returns the allowances list, not the entire JSON object.

### `save_records(section, records)` (lines 33–44)

This function replaces one section in `data.json` while preserving the other sections.

- **Line 33:** Defines the function. It takes a section name and the list of records to save.
- **Line 34:** Describes its purpose.
- **Line 35:** Checks that the requested section is allowed.
- **Line 36:** Raises an error if it is not.
- **Line 37:** Checks that `records` is a Python list.
- **Line 38:** Raises a `TypeError` if it is not a list.
- **Line 40:** Loads the existing JSON object, including all sections.
- **Line 41:** Replaces only the requested section's value in memory.
- **Line 42:** Opens `data.json` in write mode (`"w"`). This replaces the file's previous contents.
- **Line 43:** Writes the full data object as formatted JSON. `indent=2` makes the file easier to read; `ensure_ascii=False` allows non-ASCII characters to be written directly.
- **Line 44:** Adds a newline at the end of the file.

For example, saving allowances loads the whole JSON object, replaces its `allowances` list, and writes the whole object back. Other sections remain in the object.

## `main.py`

This file runs the command-line interface. It shows the menu, receives input, calls the relevant functions, and saves changes through the data-storage helpers and classes.

### Imports and section names (lines 1–12)

- **Line 1:** A docstring describing this file as the command-line entry point.
- **Line 3:** Imports `date`, used to supply and validate payroll dates.
- **Line 5:** Imports `load_records` and `save_records` to read and write sections of `data.json`.
- **Line 6:** Imports department-specific loading and saving functions from `department.py`.
- **Lines 7–8:** Import the project's classes from `oop_prac.py`: departments, employees, positions, salary scales, allowances, deductions, payrolls, and payslips.
- **Line 10:** Stores the section name `"allowances"` in a constant.
- **Line 11:** Stores the section name `"payroll_roster"` in a constant.
- **Line 12:** Stores the section name `"payrolls"` in a constant.

These constants avoid repeating the same section-name strings in several places.

### Loading employees (lines 15–31)

- **Line 15:** Defines `load_employees(scale)`. It converts saved employee records into `Employee` objects. The comment on this line has spelling mistakes; in plain terms, the function loads valid employees from the departments.
- **Line 16:** Starts an empty list for the resulting employee objects.
- **Line 17:** Loads all departments and starts looping through them.
- **Line 18:** Loops through the saved staff records for the current department.
- **Line 19:** Checks whether a staff record is a dictionary.
- **Line 20:** Skips it if it is not. `continue` moves to the next loop item.
- **Line 21:** Gets the employee's saved position title. If it is missing, assumes `"regular worker"`.
- **Line 22:** Checks that the title is text.
- **Line 23:** Skips the record if the title is not text.
- **Line 24:** Checks that the title is a recognized `Position` title and exists in the supplied salary scale.
- **Line 25:** Skips records that fail either check.
- **Line 26:** Creates a `Position` object using the title, the current department's name, and that title's salary from `scale`.
- **Line 27:** Starts a `try` block because the saved employee record might have missing or invalid values.
- **Line 28:** Builds an `Employee` object from the saved record and the `Position` object, then adds it to `result`.
- **Line 29:** Catches invalid-value and type errors raised while building the employee.
- **Line 30:** Prints a message identifying a record that could not be loaded. It shows the ID if available, or `?` if not.
- **Line 31:** Returns the successfully loaded `Employee` objects.

### Keeping the active payroll roster current (lines 34–47)

- **Line 34:** Defines `sync_payroll_roster(scale)`.
- **Line 35:** The docstring says the function keeps the roster synchronized with active employees.
- **Line 36:** Starts an empty roster list.
- **Line 37:** Loads employee objects and loops through them.
- **Line 38:** Checks whether the employee's status is `"active"`.
- **Lines 39–45:** For each active employee, adds a dictionary to the roster containing their ID, name, position title, department, and monthly salary.
- **Line 46:** Saves the rebuilt roster to the `payroll_roster` section. This replaces the old roster with the current active employees.
- **Line 47:** Returns the roster list.

The roster is a saved summary of active employees. The employee records themselves remain under their departments' `staff` lists.

### Showing the roster (lines 50–59)

- **Line 50:** Defines `show_payroll_roster(scale)`.
- **Line 51:** Calls `sync_payroll_roster` first so it displays a freshly built roster.
- **Line 52:** Checks whether the roster is empty.
- **Lines 53–54:** Prints a message and exits the function if no active employees were found.
- **Line 55:** Prints a heading.
- **Line 56:** Loops through the roster records.
- **Lines 57–59:** Prints each employee's ID, name, position, department, and monthly salary. The `:,.2f` format displays commas and two decimal places.

### Choosing a department (lines 62–73)

- **Line 62:** Defines `select_department(departments)`.
- **Line 63:** Checks whether the supplied list is empty.
- **Lines 64–65:** Prints a message and returns `None` if there are no departments to choose from.
- **Line 66:** Prints a heading.
- **Line 67:** Loops through the departments with `enumerate`. `start=1` makes the displayed numbering begin at 1.
- **Line 68:** Prints each department's number and name.
- **Line 69:** Asks the user for a department number and removes spaces at the beginning or end with `.strip()`.
- **Line 70:** Checks that the input contains digits and that the number is within the valid range.
- **Lines 71–72:** Prints an error and returns `None` for an invalid choice.
- **Line 73:** Returns the selected department. Subtracting 1 converts the user's number to a Python list index, which starts at 0.

### Adding a department (lines 76–84)

- **Line 76:** Defines `add_department(departments)`.
- **Line 77:** Prompts for a department name and removes surrounding spaces.
- **Line 78:** Starts a `try` block.
- **Line 79:** Calls the `Department` class method to create a department and add it to the list.
- **Line 80:** Catches a `ValueError`, such as an empty or duplicate department name.
- **Lines 81–82:** Prints the error and exits the function.
- **Line 83:** Saves the updated department list.
- **Line 84:** Confirms the department was added.

### Adding an employee (lines 87–124)

- **Line 87:** Defines `add_employee(departments, scale)`.
- **Line 88:** Gets a new employee ID from `Employee.generate_id()`.
- **Line 89:** Shows the generated ID to the user.
- **Line 90:** Gets the allowed position titles from `Position.TITLES`.
- **Line 91:** Prints a heading.
- **Line 92:** Loops through the titles and numbers them from 1.
- **Line 93:** Shows each title and its current salary from `scale`.
- **Line 94:** Asks the user to choose a position number.
- **Line 95:** Checks that the input is a valid number within the available choices.
- **Lines 96–97:** Prints an error and exits if the choice is invalid.
- **Line 98:** Calls `select_department` so the employee can be assigned to a department.
- **Lines 99–100:** Exits if no department was selected.
- **Line 101:** Converts the position number into the matching title.
- **Line 102:** Creates a `Position` object with the chosen title, department name, and salary.
- **Line 103:** Starts a `try` block around employee creation and user input.
- **Line 104:** Asks whether the employee is a tax resident in Uganda. `.casefold()` makes the answer lowercase for comparison.
- **Line 105:** Treats `"n"` and `"no"` as not resident. Other answers, including a blank answer, count as resident.
- **Lines 106–115:** Creates the `Employee` object from the generated ID, the user's details, the position object, and the tax-residency answer. Line 112 uses `"active"` if the user leaves status blank.
- **Line 116:** Catches invalid values, such as a date in the wrong format.
- **Lines 117–118:** Prints the error and exits without saving the employee.
- **Line 119:** Converts the employee object to a dictionary and adds that dictionary to the department's staff list.
- **Line 120:** Saves the departments, including the new staff record.
- **Line 121:** Confirms the employee was added and displays the salary.
- **Line 122:** Checks whether the new employee is active.
- **Lines 123–124:** If active, rebuilds and saves the payroll roster, then confirms the employee is on it.

### Listing employees (lines 127–135)

- **Line 127:** Defines `show_employees(scale)`.
- **Line 128:** Loads valid employee objects.
- **Line 129:** Checks whether any employees were loaded.
- **Lines 130–131:** Prints a message and exits if the list is empty.
- **Line 132:** Loops through the employees.
- **Lines 133–135:** Prints each employee's ID, name, position, department, status, salary, and calculated age.

### Adding an allowance (lines 138–159)

- **Line 138:** Defines `add_allowance(scale)`.
- **Line 139:** Loads employee objects so the program can check the entered employee ID.
- **Line 140:** Asks which employee should receive the allowance.
- **Line 141:** Sets a flag to `False`. It changes if the employee is found.
- **Lines 142–145:** Searches the employee list. It compares IDs without regard to letter case; if it finds a match, it sets the flag and stops searching.
- **Lines 146–148:** Prints a message and exits if no employee has that ID.
- **Line 149:** Asks for the allowance name.
- **Line 150:** Starts a `try` block for checking the amount and creating the allowance.
- **Line 151:** Reads the amount as a floating-point number.
- **Line 152:** Generates an allowance ID, creates an `Allowance` object, and associates it with the entered employee ID.
- **Line 153:** Catches a `ValueError`, for example if the amount cannot be converted to a number or fails the class's validation.
- **Lines 154–155:** Prints the error and exits.
- **Line 156:** Loads the existing allowances list.
- **Line 157:** Converts the new allowance object to a dictionary and appends it to the list.
- **Line 158:** Saves the updated list.
- **Line 159:** Confirms the allowance was added.

### Removing an employee and their records (lines 162–231)

- **Line 162:** Defines `remove_employee(scale)`.
- **Line 163:** Loads employees.
- **Line 164:** Checks whether there are any.
- **Lines 165–166:** Prints a message and exits if there are none.
- **Line 168:** Prints a heading.
- **Lines 169–170:** Lists employee IDs, names, and departments.
- **Line 171:** Asks which employee to remove and converts the entered ID to lowercase.
- **Line 173:** Initializes `selected` to `None`, meaning no employee has been selected yet.
- **Lines 174–177:** Searches employees for a matching ID and stores the matching object in `selected`.
- **Lines 178–180:** Prints an error and exits if no match was found.
- **Lines 182–184:** Asks for confirmation before removing related data.
- **Lines 185–187:** Cancels unless the answer is `"y"` or `"yes"`.
- **Line 189:** Comment describing removal from department staff.
- **Line 190:** Loads departments so their staff lists can be updated.
- **Lines 191–192:** Loops through departments and asks each one to remove the selected employee's staff record.
- **Line 193:** Saves the updated departments.
- **Line 195:** Comment describing allowance cleanup.
- **Line 196:** Starts a list for allowances to keep.
- **Line 197:** Loops through saved allowance records.
- **Lines 198–199:** Keeps only allowances assigned to a different employee.
- **Line 200:** Saves that filtered list, removing the selected employee's allowances.
- **Line 202:** Comment describing roster cleanup.
- **Line 203:** Starts a new roster list.
- **Line 204:** Loops through roster records.
- **Lines 205–206:** Keeps records belonging to other employees.
- **Line 207:** Saves the roster without the selected employee.
- **Line 209:** Comment describing removal of payslips and recalculation of payroll totals.
- **Line 210:** Starts a list of payroll runs to keep.
- **Line 211:** Loops through saved payroll runs.
- **Line 212:** Starts a list of payslips to keep for the current run.
- **Line 213:** Loops through that run's payslips.
- **Lines 214–215:** Keeps payslips belonging to other employees.
- **Lines 216–217:** Skips a payroll run if no payslips remain, removing that now-empty run.
- **Line 219:** Replaces the run's payslip list with the remaining slips.
- **Line 220:** Updates the employee count.
- **Line 221:** Recalculates total gross pay from the remaining payslips.
- **Lines 222–223:** Recalculates total employee deductions.
- **Lines 224–225:** Recalculates employer NSSF.
- **Line 226:** Recalculates total net pay.
- **Line 227:** Adds the updated payroll run to the list to keep.
- **Line 228:** Saves the resulting payroll list.
- **Line 230:** Rebuilds the active payroll roster from the remaining employee records.
- **Line 231:** Confirms the employee and connected records were removed.

### Editing salary scales (lines 234–254)

- **Line 234:** Defines `edit_salary_scale(scale)`.
- **Line 235:** Prints a heading.
- **Lines 236–237:** Lists each position title and its current salary.
- **Line 238:** Asks which position to edit. Pressing Enter with no value cancels.
- **Lines 239–240:** Returns if the user cancels.
- **Line 241:** Checks that the choice is a valid position number.
- **Lines 242–243:** Prints an error and returns if it is not valid.
- **Line 244:** Finds the selected position title.
- **Line 245:** Starts error handling for the new salary.
- **Line 246:** Reads the new salary as a number.
- **Lines 247–248:** Rejects a negative salary by raising a `ValueError`.
- **Lines 249–251:** Catches an invalid number or negative salary, prints the problem, and returns.
- **Line 252:** Changes that title's salary in the in-memory `scale` dictionary.
- **Line 253:** Saves the complete salary scale.
- **Line 254:** Tells the user that the new salary applies to future payroll runs.

### Running payroll (lines 257–302)

- **Line 257:** Defines `run_payroll(scale)`.
- **Line 258:** Rebuilds the roster so it reflects current active employees.
- **Line 259:** Starts an empty list of roster IDs.
- **Lines 260–261:** Copies each roster ID into that list in lowercase.
- **Line 262:** Starts an empty list of employees to pay.
- **Lines 263–265:** Loads employees and keeps only those who are active and present in the roster.
- **Lines 266–268:** If there are no employees to pay, prints a message and exits.
- **Line 269:** Asks for the payroll date. The default shown is today's date.
- **Lines 270–271:** Uses today's date if the user enters nothing.
- **Line 272:** Starts date validation.
- **Line 273:** Tries to parse the date in ISO format, `YYYY-MM-DD`.
- **Lines 274–276:** If parsing fails, prints the required format and exits.
- **Line 277:** Loads saved payroll runs.
- **Line 278:** Generates the next payroll ID.
- **Line 279:** Starts an empty list of allowance objects.
- **Line 280:** Loads saved allowance records and loops through them.
- **Line 281:** Checks that each record is a dictionary.
- **Line 282:** Converts valid dictionaries to `Allowance` objects and adds them to the list.
- **Line 283:** Starts an empty list of payslips for this run.
- **Line 284:** Loops through the active employees to pay.
- **Line 285:** Starts a list for the current employee's allowances.
- **Lines 286–288:** Finds allowances belonging to this employee and adds them to that list.
- **Line 289:** Adds up this employee's allowance amounts.
- **Line 290:** Checks whether the employee's age is from 16 through 55 for NSSF eligibility.
- **Lines 291–292:** Creates a `Deductions` object using salary, allowances, tax-residency status, and NSSF eligibility.
- **Line 293:** Creates a `Payslip` using the employee, payroll details, their allowances, and deductions; adds it to the payslip list.
- **Line 294:** Creates a `Payroll` containing all the payslips for this run.
- **Line 295:** Converts that payroll to a dictionary and appends it to the saved payroll records.
- **Line 296:** Saves the updated payroll list.
- **Line 297:** Prints the payroll ID and date.
- **Line 298:** Prints how many payslips were created.
- **Lines 299–302:** Print total gross pay, employee deductions, employer NSSF, and net pay, calculated from the payroll's payslips.

### Showing a payslip (lines 305–317)

- **Line 305:** Defines `show_payslip()`.
- **Line 306:** Loads saved payroll runs.
- **Line 307:** Asks which payroll run to look in.
- **Line 308:** Asks which employee's payslip to show.
- **Line 309:** Searches the payroll records.
- **Line 310:** Checks whether a payroll record has the requested payroll ID.
- **Line 311:** Loops through that payroll's payslips.
- **Line 312:** Compares each payslip's employee ID with the requested ID, ignoring letter case.
- **Line 313:** Recreates a `Payslip` object from the saved dictionary and displays it.
- **Line 314:** Exits after displaying the matching payslip.
- **Lines 315–316:** If the payroll exists but has no payslip for that employee, prints that message and exits.
- **Line 317:** If no payroll with that ID was found, prints that the payroll run was not found.

### Starting the program and displaying the menu (lines 320–371)

- **Line 320:** Defines `main()`, which prepares the program and runs the menu.
- **Line 321:** Loads the departments.
- **Line 322:** Saves them, ensuring the department data is written in the expected format.
- **Line 323:** Loads the salary scale.
- **Lines 324–325:** Checks every known position title and adds its default salary if it is missing from the loaded scale.
- **Line 326:** Saves the completed salary scale.
- **Line 327:** Builds and saves the current active payroll roster.
- **Line 328:** Starts a loop that continues until the user chooses Exit.
- **Line 329:** Prints the menu heading.
- **Lines 330–340:** Print the numbered menu choices.
- **Line 341:** Reads the user's choice and strips surrounding spaces.
- **Lines 342–344:** For choice `"1"`, lists the departments currently in memory.
- **Lines 345–346:** For choice `"2"`, calls the function to add a department.
- **Lines 347–348:** For choice `"3"`, calls the function to add an employee.
- **Lines 349–350:** For choice `"4"`, lists employees.
- **Lines 351–352:** For choice `"5"`, displays the active payroll roster.
- **Lines 353–354:** For choice `"6"`, removes an employee and their related records.
- **Lines 355–356:** For choice `"7"`, adds an employee allowance.
- **Lines 357–358:** For choice `"8"`, edits the salary scale.
- **Lines 359–360:** For choice `"9"`, runs payroll.
- **Lines 361–362:** For choice `"10"`, displays a payslip.
- **Lines 363–365:** For choice `"11"`, prints a goodbye message and uses `break` to end the menu loop.
- **Lines 366–367:** If the choice does not match, asks the user to choose a number from 1 to 11.
- **Lines 370–371:** This is Python's entry-point check. When `main.py` is run directly, `__name__` is `"__main__"`, so it calls `main()`. If another file imports `main.py`, the menu does not start automatically.

## How the two files work together

`main.py` decides what action to perform based on the user's menu choice. When it needs saved data, it calls helpers such as `load_records` and `save_records`. Those helpers in `data_store.py` read or update the appropriate section of `data.json`.

For example, adding an allowance works like this:

1. `main.py` loads the current allowances list with `load_records("allowances")`.
2. It adds the new allowance record to that Python list.
3. It calls `save_records("allowances", records)`.
4. `data_store.py` loads the full JSON object, replaces the allowances list, and writes the full object back to `data.json`.
