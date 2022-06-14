# Csv-to-Json
This is a program that takes 4 different CSV's containing data on students and creates a JSON report card based on the data given.

# Arguements
When running the main script it takes 4 command line arguements in order. Courses.csv path, Students.csv path, Tests.csv path, Marks.csv path, output path.
E.G: main.py courses.csv students.csv tests.csv marks.csv output.csv
The first row must be the column names.
The columns expected for courses csv are 'id','name','teacher'
The columns expected for students csv are 'id','name'
The columns expected for tests csv are 'id','course_id','weight'
The columns expected for marks csv are 'test_id','student_ids','mark'
