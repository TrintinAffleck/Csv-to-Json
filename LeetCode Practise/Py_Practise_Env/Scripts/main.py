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
        usecols=['test_id','student_ids','mark'])
    except ValueError:
        print("You have entered the wrong column names or order.")
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

    student_test_id_map = {}
    def get_test_ids_map(): 
        '''Gets the Test Ids from the ``marks.csv`` and returns a ``dictionary``
        with the ``key`` being the student and the ``value`` being a unique list of all the different
        tests they took. ``E.g:`` if the student with a student id of '1' took tests with test ids 1,1,2,3
        the value is [1,2,3]'''
        seen_student_ids = set()
        curr_student_values = []
        for i,row in marks_df.iterrows():
            #Init Current Student & Test Id
            curr_student = row[marks_df.columns[1]]
            curr_test_id = row[marks_df.columns[0]]
            #Updating my map with them
            if curr_student:
                student_test_id_map.update({f"{curr_student}": curr_student_values})
            else:
                print("Your row or column is empty! Check your data!") 
            #Reset the map if we see a new student 
            if curr_student not in seen_student_ids:
                curr_student_values = []
                seen_student_ids.add(curr_student)
            #If test_id isnt in our list already add it
            if curr_test_id not in curr_student_values:
                curr_student_values.append(curr_test_id)
        return student_test_id_map

    nested_dicts = {
        "id" : loaded_student,
        "name" : loaded_student,
        "totalAverage" : 0,
        "courses" : [loaded_courses]
    }
    for item in get_test_ids_map().items():
        student,test_taken = item
        student_courses_map = {}
        student_courses = []
        for row in tests_df.itertuples(index=False):
            id,course_id,weight = row
            if id in test_taken:
                #Add this course to this students course list
                if str(course_id) not in student_courses_map.get(student,[]):
                    if course_id not in student_courses:
                        student_courses.append(course_id)
                        student_courses_map.update({student : student_courses})
        #Adding totalAverage and courses keys into json
        for i in range(len(loaded_student)):
            loaded_student[i].update({'totalAverage' : 0, 'courses' : student_courses})


    report = {
        "students" : loaded_student,
        "error" : "Invalid course weights"
    }

    dumped = dumps(report,indent=2)
    # print(dumped)
    f = open('test.txt','w')
    f.write(dumped)
    f.close()

if __name__ == '__main__':
    main()