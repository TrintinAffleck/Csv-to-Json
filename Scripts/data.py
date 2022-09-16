from pandas import read_csv
from command_inputs import Commands as paths
class Data():
    #Creating Dataframes
    try:
        courses_df = read_csv(paths.course_path, engine='python',header=0,
        usecols=['id','name','teacher'])
        students_df = read_csv(paths.students_path, engine='python',header=0,
        usecols=['id','name'])
        tests_df = read_csv(paths.tests_path, engine='python',header=0,
        usecols=['id','course_id','weight'])
        marks_df = read_csv(paths.marks_path, engine='python',header=0,
        usecols=['test_id','student_id','mark'])
    except ValueError:
        print("You have either entered the wrong column names or order.")
        print(f"The columns we expected for the courses csv are {['id','name','teacher']}")
        print(f"The columns we expected for the students csv are {['id','name']}")
        print(f"The columns we expected for the tests csv are {['id','course_id','weight']}")
        print(f"The columns we expected for the marks csv are {['test_id','student_ids','mark']}")  
    else:
        print("Csv's successfully read.")