#Built-Ins
'''Some of these are in other files'''
from json import dumps

#Locals
from data import Data
from convert import Json

#3rd Party
import pandas as pd

#Global variables
student_test_id_dict = {}
student_avg_mark_dict = {}
test_id_marks_dict = {}
marks = []        
tests_taken = []        
seen_student = set()
def main():

    def get_avg(numbers: list):
        if len(numbers) > 0:
            return round((sum(numbers) / len(numbers)),2)
        return 0

    def create_dicts(student_index:int): 
        
        student_df = Data.marks_df.groupby('student_id').get_group(student_index+1)

        for row in student_df.itertuples(index=False):
            test_id,curr_student,mark = row
            if test_id not in tests_taken:
                tests_taken.append(test_id)
            #Clear our lists because we dont want a previous students tests to overlap with the current students tests.
            #Didn't use .clear() because it overlaps with the next student if there is one.
            #Create Marks list to keep track of student marks.
            marks.append(mark)
            if len(marks) > 0:
                average_mark = get_avg(marks)
                student_avg_mark_dict.update({f"{curr_student}": round(average_mark,2)})
                if test_id not in test_id_marks_dict.keys():
                    test_id_marks_dict.update({test_id: mark})
            #We need a list of test_ids for the dictionary.
        if student_index not in seen_student:
            seen_student.add(student_index)
        return student_test_id_dict
    
    def update_student_keys(courses_taken:list, courses:list, index:int,averages):
        student = Json.loaded_student[index]
        total_avg = Data.marks_df.groupby('student_id').mark.mean().loc[student.get('id')]
        for course in Json.loaded_courses:
            if course.get('id') in courses_taken:
                courses.append(course)
                student.update({'totalAverage' : round(total_avg,2),
                                'courses' : courses})
                course.update({'courseAverage' : averages[course['id']]})
        return courses

    def get_courses_and_tests():
        '''Returns true if weights are not 100.'''
        student_index = 0
        create_dicts(student_index)
        total_weight = 0
        courses_taken = []
        courses_avg_dict = {}
        course_avg = 0.0
        courses = []
        marks_list = []

        for row in Data.tests_df.itertuples(index=False):
            test_id,course_id,weight = row
            if test_id in tests_taken:
                if course_id not in courses_taken:
                    courses_avg_dict[course_id] = 0
                    courses_taken.append(course_id)
                    marks_list = []
                    #Weight cant be lower than 100 percent. So we throw an error key.
                    if total_weight < 100 and total_weight != 0:
                        print("Weight error: Course weights are under 100.")
                        return True
                    total_weight = 0
                marks_list.append(test_id_marks_dict.get(test_id))
                course_avg = get_avg(marks_list)
                courses_avg_dict.update({course_id : course_avg})
                update_student_keys(courses_taken,courses,student_index,courses_avg_dict)
                total_weight += weight
                #Weight cant be higher than 100 percent. So we throw an error key.
                if total_weight > 100:
                    print("Weight error: Course weights are over 100.")
                    return True
        #So we can look at the data for the next student
        student_index+=1
        #Clearing variables for the new student
        test_id_marks_dict.clear()
        tests_taken.clear()
        create_dicts(student_index)
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