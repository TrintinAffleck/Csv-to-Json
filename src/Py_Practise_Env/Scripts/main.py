#Built-Ins
'''Some of these are in other files'''
from json import dumps

#Locals
from data import Data
from convert import Json

#3rd Party

#Global variables
student_test_id_dict = {}
student_avg_mark_dict = {}
seen_student = set()
test_id_marks_dict = {}
tests_taken = []        
marks = []        
marks_list = []
courses_taken = []
courses_avg_dict = {}
courses = []

def main():
    student_index = 0
    def get_avg(numbers: list):
        if len(numbers) > 0:
            return round((sum(numbers) / len(numbers)),2)
        return 0

    def create_dicts(student_index:int):
        '''Creates tests_taken, avg mark, student_avg_mark_dict, test_id_marks_dict,
         and returns student_test_id_dict'''
        student_df = Data.marks_df.groupby('student_id').get_group(student_index)
        for row in student_df.itertuples(index=False):
            test_id,curr_student,mark = row
            if test_id not in tests_taken:
                tests_taken.append(test_id)
            marks.append(mark)
            if len(marks) > 0:
                average_mark = get_avg(marks)
                student_avg_mark_dict.update({f"{curr_student}": round(average_mark,2)})
                if test_id not in test_id_marks_dict.keys():
                    test_id_marks_dict.update({test_id: mark})
        if student_index not in seen_student:
            seen_student.add(student_index)
        return student_test_id_dict
    
    
    def error_check(courses_taken:list,tests_taken:list,total_weight:float or int = 0):
        seen_course = []
        for row in Data.tests_df.itertuples(index=False):
            test_id,course_id,weight = row
            if test_id in tests_taken:
                if course_id in courses_taken and course_id not in seen_course:
                    seen_course.append(course_id)
                    #Weight cant be lower than 100 percent. Return True.
                    if total_weight < 100 and total_weight != 0:
                        print("Weight error: Course weights are under 100.")
                        return True
                    total_weight = 0
                total_weight += weight
                #Weight cant be higher than 100 percent. Return True.
                if total_weight > 100:
                    print("Weight error: Course weights are over 100.")
                    return True

    def update_student_keys(courses_taken:list, 
                            courses:list, 
                            index:int,
                            averages
                            ):
        student = Json.loaded_student[index-1]
        df = Data.marks_df
        total_avg = df.groupby('student_id').mark.mean().loc[student.get('id')]
        for course in Json.loaded_courses:
            if course.get('id') in courses_taken:
                courses.append(course)
                course.update({'courseAverage' : averages[course['id']]})
                student.update({'totalAverage' : round(total_avg,2),'courses' : courses})
        return courses

    def get_courses():
        for row in Data.tests_df.itertuples(index=False):
            test_id,course_id,weight = row
            if test_id in tests_taken:
                if course_id not in courses_taken:
                    courses_taken.append(course_id)
                    marks_list = []
                marks_list.append(test_id_marks_dict.get(test_id))
                course_avg = get_avg(marks_list)
                courses_avg_dict.update({course_id : course_avg})

    for student in range(len(Data.students_df.groupby('id'))):
        student_index+=1
        create_dicts(student_index)
        get_courses()
        if error_check(courses_taken,tests_taken) == True:
            break
        update_student_keys(courses_taken,[],student_index,courses_avg_dict)
        #Clearing variables for the next student
        courses.clear()
        courses_avg_dict.clear()
        courses_taken.clear()
        test_id_marks_dict.clear()
        tests_taken.clear()
    
if __name__ == '__main__':
    if  main() == True:
        report = {'error' : 'Invalid course weights'}
    else:
        report = {'students' : Json.loaded_student}

    dumped = dumps(report,indent=2)
    f = open('output.json','w')
    f.write(dumped)
    f.close()