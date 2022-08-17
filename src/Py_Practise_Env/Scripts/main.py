#Built-Ins
'''Some of these are in other files'''
from json import dumps

#Locals
from data import Data
from convert import Json

#Global variables
student_test_id_dict = {}
student_avg_mark_dict = {}
test_id_marks_dict = {}
marks = []
def main():

    def get_avg(numbers: list):
        if len(numbers) > 0:
            return round((sum(numbers) / len(numbers)),2)
        return 0

    def get_student_tests(): 
        '''Gets the Test Ids from the ``marks.csv`` and returns a ``dictionary``
        with the ``key`` being the student and the ``value`` being a unique list of all the different
        tests they took. ``E.g:`` if the student with a student id of '1' took tests with test ids 1,1,2,3
        the value is [1,2,3]'''
        seen_student_ids = set()
        values = []
        for row in Data.marks_df.itertuples(index=False):
            test_id,curr_student,mark = row
            student_test_id_dict.update({f"{curr_student}": values})
            #Clear our lists because we dont want a previous students tests to overlap with the current students tests.
            #Didn't use .clear() because it overlaps with the next student if there is one.
            if curr_student not in seen_student_ids:
                values = []
                marks = []
                seen_student_ids.add(curr_student)
            #Create Marks list to keep track of student marks.
            marks.append(mark)
            if len(marks) > 0:
                average_mark = Data.marks_df.groupby('student_id').mark.mean().loc[curr_student]
                if test_id not in test_id_marks_dict.keys():
                    test_id_marks_dict.update({test_id: mark})
                student_avg_mark_dict.update({f"{curr_student}": round(average_mark,2)})
            #We need a list of test_ids for the dictionary.
            if test_id not in values:
                values.append(test_id)
        return student_test_id_dict
    

    def update_student(courses_taken:list, courses:list, index:int, average):
        student = Json.loaded_student[index]
        total_avg = Data.marks_df.groupby('student_id').mark.mean().loc[student.get('id')]
        for course in Json.loaded_courses:
            if course.get('id') in courses_taken:
                courses.append(course)
                student.update({'totalAverage' : round(total_avg,2),
                                'courses' : courses,})
        return courses

    def get_courses_and_tests():
        '''Returns true if weights are not 100.'''
        student_index = 0
        for students in get_student_tests().items():
            student,test_taken = students
            total_weight = 0
            courses_taken = []
            course_avg = 0.0
            courses = []
            course_id_averages_dict = {}
            marks_list = []

            for row in Data.tests_df.itertuples(index=False):
                test_id,course_id,weight = row
                if test_id in test_taken:
                    marks_list.append(test_id_marks_dict.get(test_id))
                    if course_id not in courses_taken:
                        courses_taken.append(course_id)
                        course_avg = get_avg(marks_list)
                        print(f"average = {course_avg}")
                        print(f"marks list = {marks_list}")
                        #TODO use pandas df methods to do this its too hard brute forcing with for loops.
                        course_id_averages_dict.update({course_id : course_avg})
                        marks_list = []

                        #Weight cant be lower than 100 percent. So we throw an error key.
                        if total_weight < 100 and total_weight != 0:
                            print("Weight error: Course weights are under 100.")
                            return True
                        total_weight = 0
                    total_weight += weight
                    #Weight cant be higher than 100 percent. So we throw an error key.
                    if total_weight > 100:
                        print("Weight error: Course weights are over 100.")
                        return True
            update_student(courses_taken,courses,student_index,course_id_averages_dict)
            student_index+=1

            # for course in update_student(courses_taken,courses):
            #     if course.get('id') in course_averages_dict.keys():
            #         course.update({'courseAverage' : round(course_averages_dict.get(course['id'],2))})

        return False
    if get_courses_and_tests() == True:
        report = {'error' : 'Invalid course weights'}
    else:
        report = {'students' : Json.loaded_student}

    dumped = dumps(report,indent=2)
    f = open('output.txt','w')
    f.write(dumped)
    f.close()

if __name__ == '__main__':
    main()