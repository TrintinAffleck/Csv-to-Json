## What is this program?
A teachers admin tool, this program generates a students report card in Json format to be easily used by the front-end. This takes csv files, parses them, calculates the students’ final grades and generates the report as a structured JSON file.
## Why use this program?
Say you are contracted to make a web app that generates a students report card. You can use this to quickly put the data into a JSON file straight from the back-end so you can use it can be used more easily by the front-end.
## The data must have these requirements.
* When running the main script it takes 4 command line arguements in order. Courses.csv path, Students.csv path, Tests.csv path, Marks.csv path, output path.
E.G: main.py courses.csv students.csv tests.csv marks.csv output.csv

* The first row must be the column names.
    * The columns expected for courses csv are "id", "name", "teacher".
    * The columns expected for students csv are "id", "name".
    * The columns expected for tests csv are "id", "course_id", "weight".
    * The columns expected for marks csv are "test_id", "student_id", "mark".

* The "student_id" column must be the following
    * An integer 1,2,3,etc.
    * First student must be 1.
    * Must be unique values.
    * Must be the value of the last student + 1 (Unless its the first student) 
    E.G student_id's are 1,2,3 respectively not 1,3,5 or 1,3,3,5

* Data types for columns are as follows.
    * id must be an int and follow the same rules as student_id.
    * name must be unique 
    * course_id must be unique
    * weights are integers
    * marks are integers
