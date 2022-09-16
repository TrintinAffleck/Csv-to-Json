from json import loads
from data import Data
class Json():
    #Putting them into json format
    student_json = Data.students_df.to_json(orient='records',indent=2)
    course_json = Data.courses_df.to_json(orient='records',indent=2)
    marks_json = Data.marks_df.to_json(orient='records',indent=2)
    tests_json = Data.tests_df.to_json(orient='records',indent=2)
    loaded_student = loads(student_json)
    loaded_courses = loads(course_json)
    loaded_marks = loads(marks_json)
    loaded_tests = loads(tests_json)