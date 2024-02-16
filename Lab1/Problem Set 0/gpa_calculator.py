from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    if not courses: 
        return 0

    total_grade_points = 0
    total_course_hours = 0

    for course in courses:
        grades = course.grades
        student_id = student.id

        if student_id in grades:
            grade_points = course.convert_grade_to_points(grades[student_id])
            total_grade_points += grade_points * course.hours
            total_course_hours += course.hours

    if total_course_hours > 0:
        return total_grade_points / total_course_hours
    else:
        return 0
