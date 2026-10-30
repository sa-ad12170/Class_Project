from cli_helpers import ask_yes_no, read_number, read_text, save_record
from oop_prac import Position


def run_position_workflow():
    while True:
        position = Position(
            read_text('Enter title: '),
            read_text('Enter department: '),
            read_number('Enter salary: '),
        )
        print(position)

        record = {
            'title': position.title,
            'department': position.department,
            'salary': position.salary,
            'status': position.status(),
        }
        save_record('positions', record, ('title', 'department'))

        if not ask_yes_no('Do you want to add another position (y/n)? '):
            break


if __name__ == '__main__':
    run_position_workflow()
