"""
Tristan Deveyra 
2057603
"""
import csv
from operator import itemgetter

#create student class
class Student:
    #initialize student information
    def __init__(self, student_id, last_name, first_name, major, disciplinary_actions = False):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.major = major
        self.disciplinary_actions = disciplinary_actions
        self.gpa = None
        self.graduation_date = None

    #Function that reads student information and creates it through format of a dictionary
    def read_student_data(file_path):
        students = {} #create empty dictionary called students
        with open(file_path, 'r') as file: #open csv file
            for row in csv.reader(file): #check every row of the CSV file
                #rows that need to be read, set equal to row variable
                student_id, last_name, first_name, major, *extra = row
                disciplinary_action = extra[0] if extra else False
                students[student_id] = Student(student_id, last_name, first_name, major, disciplinary_action)
        return students #return student dictionary
    

    #function that reads GPA data from CSV file and updates it to the class
    def read_gpa_data(file_path, students):
        with open(file_path, 'r') as file: #open gpa file
            reader = csv.reader(file) 
            for row in reader: #read in rows
                student_id, gpa = row #set rows in gpa, identify it by student ID
                students[student_id].gpa = float(gpa) #set gpa 

# Function to read graduation date data and update student objects
def read_graduation_data(file_path, students):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            student_id, graduation_date = row
            students[student_id].graduation_date = graduation_date

# Function to write a list of students to a CSV file
def write_students_to_csv(file_path, students, attributes):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(attributes)
        for student_id, student in sorted(students.items(), key=lambda x: itemgetter(1)):
            writer.writerow([student_id, student.major, student.first_name, student.last_name,
                             student.gpa, student.graduation_date, student.disciplinary_action])

# Function to filter students based on GPA, graduation, and disciplinary action
def filter_students(students, gpa_threshold=3.8):
    eligible_students = [student for student in students.values()
                         if student.gpa > gpa_threshold and not student.graduation_date and not student.disciplinary_action]
    disciplined_students = [student for student in students.values() if student.disciplinary_action]
    return eligible_students, disciplined_students

# Main program
if __name__ == "__main__":
    # Read data from CSV files
    students = Student.read_student_data('C:/Users/trist/Documents/WebScraping/Project1/StudentsMajorsList-3.csv')
    Student.read_gpa_data('C:/Users/trist/Documents/WebScraping/Project1/GPAList-1.csv', students)
    read_graduation_data('C:/Users/trist/Documents/WebScraping/Project1/GraduationDatesList-1.csv', students)

    # Process data and generate reports
    full_roster_attributes = ['Student ID', 'Major', 'First Name', 'Last Name', 'GPA', 'Graduation Date', 'Disciplinary Action']
    write_students_to_csv("FullRoster.csv", students, full_roster_attributes)

    majors = set(student.major for student in students.values())
    for major in majors:
        major_file_path = f"{major.replace(' ', '')}Students.csv"
        major_students = {student.student_id: student for student in students.values() if student.major == major}
        major_attributes = ['Student ID', 'Last Name', 'First Name', 'Graduation Date', 'Disciplinary Action']
        write_students_to_csv(major_file_path, major_students, major_attributes)

    eligible_students, disciplined_students = filter_students(students)

    scholarship_attributes = ['Student ID', 'Last Name', 'First Name', 'Major', 'GPA']
    write_students_to_csv("ScholarshipCandidates.csv", {student.student_id: student for student in eligible_students}, scholarship_attributes)

    disciplined_attributes = ['Student ID', 'Last Name', 'First Name', 'Graduation Date']
    write_students_to_csv("DisciplinedStudents.csv", {student.student_id: student for student in disciplined_students}, disciplined_attributes)