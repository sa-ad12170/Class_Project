from storage import StorageError, append_record


def read_text(prompt):
    """Read a required text value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('This value is required.')


def read_number(prompt, minimum=0, maximum=None, integer=False):
    """Read a number within the requested range."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value) if integer else float(value)
        except ValueError:
            print('Enter a valid number.')
            continue

        if number < minimum:
            print(f'Value must be at least {minimum}.')
            continue
        if maximum is not None and number > maximum:
            print(f'Value cannot exceed {maximum}.')
            continue
        return number


def ask_yes_no(prompt):
    """Return True for yes and False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in {'y', 'yes'}:
            return True
        if answer in {'n', 'no'}:
            return False
        print('Enter y for yes or n for no.')


def save_record(collection, record, unique_fields):
    """Save one CLI record and display a friendly result."""
    try:
        append_record(collection, record, unique_fields)
        print('Record saved successfully')
        return True
    except StorageError as error:
        print(error)
        return False
