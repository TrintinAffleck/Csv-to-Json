from cgi import test
from sys import argv,exit
from pandas import read_csv
from json import loads,dumps
from glob import glob;
def main():
    '''Setting up CLI'''
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

    #Find files csv files in directory
    file_ext = ".csv"
    all_files = [i for i in glob(f"*{file_ext}")]

    #Creating Dataframes
    try:
        courses_df = read_csv(course_path, engine='python',header=0,
        usecols=['id','name','teacher'])
        students_df = read_csv(students_path, engine='python',header=0,
        usecols=['id','name'])
        tests_df = read_csv(tests_path, engine='python',header=0,
        usecols=['id','course_id','weight'])
        marks_df = read_csv(marks_path, engine='python',header=0,
        usecols=['test_id','student_id','mark'])
    except ValueError:
        print("You have either entered the wrong column names or order.")
        print(f"The columns we expected for the courses csv are {['id','name','teacher']}")
        print(f"The columns we expected for the students csv are {['id','name']}")
        print(f"The columns we expected for the tests csv are {['id','course_id','weight']}")
        print(f"The columns we expected for the marks csv are {['test_id','student_ids','mark']}")  
    else:
        print("Csv's successfully read.")

    #Putting them into json format
    student_json = students_df.to_json(orient='records',indent=2)
    course_json = courses_df.to_json(orient='records',indent=2)
    marks_json = marks_df.to_json(orient='records',indent=2)
    tests_json = tests_df.to_json(orient='records',indent=2)
    loaded_student = loads(student_json)
    loaded_courses = loads(course_json)
    loaded_marks = loads(marks_json)
    loaded_tests = loads(tests_json)

    def get_test_ids_map(): 
        '''Gets the Test Ids from the ``marks.csv`` and returns a ``dictionary``
        with the ``key`` being the student and the ``value`` being a unique list of all the different
        tests they took. ``E.g:`` if the student with a student id of '1' took tests with test ids 1,1,2,3
        the value is [1,2,3]'''
        student_test_id_map = {}
        seen_student_ids = set()
        curr_student_values = []
        marks = []
        for row in marks_df.itertuples(index=False):
            #find avg
            #update dict
            test_id,curr_student,mark = row
            student_test_id_map.update({f"{curr_student}": curr_student_values})
            #Reset the map if we see a new student
            if curr_student not in seen_student_ids:
                curr_student_values = []
                marks = []
                seen_student_ids.add(curr_student)
            if len(marks) > 0:
                average_mark = (sum(marks) / len(marks))
            marks.append(mark)
            #If test_id isnt in our list already add it
            if test_id not in curr_student_values:
                curr_student_values.append(test_id)
        return student_test_id_map

    #TODO Maybe refactor this too    
    def get_courses_and_tests(item_index: int = 0, course_index: int = 0):
        for item in get_test_ids_map().items():
            student,test_taken = item
            tests_list = []
            for row in tests_df.itertuples(index=False):
                test_id,course_id,weight = row
                if test_id in test_taken:
                    if course_id not in tests_list:
                        tests_list.append(course_id)

            curr_student = loaded_student[item_index]
            courses = []
            #Adding totalAverage and courses keys into json
            for i in range(len(loaded_courses)):
                if loaded_courses[i]['id'] in tests_list:
                    courses.append(loaded_courses[i])
                    curr_student.update({'totalAverage' : 0,'courses' : courses})
                course_index+=1
            item_index+=1
            course_index=0
    get_courses_and_tests()

    report = {
        'students' : loaded_student,
        'error' : 'Invalid course weights'
    }

    dumped = dumps(report,indent=2)
    #print(dumped)
    f = open('output.txt','w')
    f.write(dumped)
    f.close()

if __name__ == '__main__':
    main()