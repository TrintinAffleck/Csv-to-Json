#Built-Ins
from json import loads,dumps

#Locals
from command_inputs import Commands as paths
from data import Data
from convert import Json
def main():
    student_test_id_map = {}
    student_marks = {}
    def create_dict(): 
        '''Gets the Test Ids from the ``marks.csv`` and returns a ``dictionary``
        with the ``key`` being the student and the ``value`` being a unique list of all the different
        tests they took. ``E.g:`` if the student with a student id of '1' took tests with test ids 1,1,2,3
        the value is [1,2,3]'''
        seen_student_ids = set()
        marks = []
        values = []
        for row in Data.marks_df.itertuples(index=False):
            test_id,curr_student,mark = row
            student_test_id_map.update({f"{curr_student}": values})
            #Clear our lists because we dont want a previous students tests to overlap with the current students tests.
            if curr_student not in seen_student_ids:
                values.clear()
                marks.clear()
                seen_student_ids.add(curr_student)
            #Create Marks list to keep track of student marks.
            marks.append(mark)
            if len(marks) > 0:
                average_mark = (sum(marks) / len(marks))
                student_marks.update({f"{curr_student}": average_mark})
            #We need a list of test_ids for the dictionary.
            if test_id not in values:
                values.append(test_id)
        return student_test_id_map

    #TODO Maybe refactor this too    
    def get_courses_and_tests(item_index: int = 0, course_index: int = 0):
        for item in create_dict().items():
            student,test_taken = item
            tests_list = []
            for row in Data.tests_df.itertuples(index=False):
                test_id,course_id,weight = row
                if test_id in test_taken:
                    if course_id not in tests_list:
                        tests_list.append(course_id)

            curr_student = Json.loaded_student[item_index]
            courses = []
            #Adding totalAverage and courses keys into json
            for i in range(len(Json.loaded_courses)):
                if Json.loaded_courses[i]['id'] in tests_list:
                    courses.append(Json.loaded_courses[i])
                    curr_student.update({'totalAverage' : 0,'courses' : courses})
                course_index+=1
            item_index+=1
            course_index=0
    get_courses_and_tests()

    report = {
        'students' : Json.loaded_student,
        'error' : 'Invalid course weights'
    }

    dumped = dumps(report,indent=2)
    #print(dumped)
    f = open('output.txt','w')
    f.write(dumped)
    f.close()

if __name__ == '__main__':
    main()