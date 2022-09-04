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
test_id_marks_dict = {}
marks = []
def main():

    def get_avg(numbers: list):
        if len(numbers) > 0:
            return round((sum(numbers) / len(numbers)),2)
        return 0

    def get_student_tests(): 
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
                student.update({'totalAverage' : round(total_avg,2),
                                'courses' : courses})
                course.update({'courseAverage' : averages[course['id']]})
        return courses

    def get_courses_and_tests():
        '''Returns true if weights are not 100.'''
        student_index = 0
        total_weight = 0
        courses_taken = []
        courses_avg_dict = {}
        course_avg = 0.0
        courses = []
        marks_list = []
        for row in Data.tests_df.itertuples(index=False):
            test_id,course_id,weight = row
            if test_id in tests_taken:
                #TODO Problem is if student skips the a test and the next one taken is in not a new course the total weight is not reset
                if course_id not in courses_taken:
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
                total_weight += weight
                #Weight cant be higher than 100 percent. So we throw an error key.
                if total_weight > 100:
                    print("Weight error: Course weights are over 100.")
                    return True

        for student in range(len(Data.students_df.groupby('id'))):
            student_index+=1
            create_dicts(student_index)
            update_student_keys(courses_taken,courses,student_index,courses_avg_dict)
            #Clearing variables for the new student
            test_id_marks_dict.clear()
            tests_taken.clear()

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