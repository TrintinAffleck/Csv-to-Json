#Built-Ins
'''Some of these are in other files'''
from json import dumps

#Locals
from data import Data
from convert import Json
def main():
    student_test_id_map = {}
    student_marks = {}
    invalid = False #For invalid course weights
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
            #Didn't use .clear() because it overlaps with the next student if there is one.
            if curr_student not in seen_student_ids:
                values = []
                marks = []
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

    def get_courses_and_tests(item_index: int = 0, course_index: int = 0):
        courses_dict = {}
        for item in create_dict().items():
            total_weight = 0
            student,test_taken = item
            courses_taken = []
            for row in Data.tests_df.itertuples(index=False):
                test_id,course_id,weight = row
                if test_id in test_taken:
                    #Reset the total weight to 0 whenever we see a new course so the course weights dont overlap.
                    if course_id not in courses_taken:
                        courses_taken.append(course_id)
                        total_weight = 0
                    total_weight += weight
                        
            #Weight cant possibly be higher than 100 percent. So we throw an error key
            if total_weight > 100:
                print("Weights over 100")
                invalid = True 

            curr_student = Json.loaded_student[item_index]
            courses = []
            #Adding totalAverage and courses keys into json
            for i in range(len(Json.loaded_courses)):
                if Json.loaded_courses[i]['id'] in courses_taken:
                    courses.append(Json.loaded_courses[i])
                    curr_student.update({'totalAverage' : round(student_marks[student],2),'courses' : courses})
                course_index+=1
            item_index+=1
            course_index=0
    get_courses_and_tests()
    if invalid == True:
        report = {'students' : Json.loaded_student,
                  'error' : 'Invalid course weights'}
    else:
        report = {'students' : Json.loaded_student}
    dumped = dumps(report,indent=2)
    #print(dumped)
    f = open('output.txt','w')
    f.write(dumped)
    f.close()

if __name__ == '__main__':
    main()