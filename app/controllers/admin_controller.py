# admin_controller.py

from app.models import user_student, enrollment, auth

def search_student_by_id(student_id):
    return user_student.get_student_by_id(student_id)

def search_students_by_name(name):
    return user_student.get_students_by_name(name)

def filter_students_by_subject(subject):
    return enrollment.get_students_by_subject(subject)

def fetch_login_statistics():
    authentication = auth.Authentication()
    return authentication.get_login_statistics()
