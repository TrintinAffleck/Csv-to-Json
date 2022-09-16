from sys import argv

class Commands():
    argument_list = argv[1:]
    if len(argument_list) == 5:
        course_path = argument_list[0]
        students_path = argument_list[1]
        tests_path = argument_list[2]
        marks_path = argument_list[3]
        output_path = argument_list[4]
    else:
        print(f"Arguements given: {len(argument_list)} Expected 5")
        exit(0)