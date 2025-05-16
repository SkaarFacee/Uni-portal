# admin_view.py

from app.controllers import admin_controller


def search_student_by_id_view():
    student_id = input("Enter Student ID: ")
    student = admin_controller.search_student_by_id(student_id)
    if student:
        print("Student Found:", student)
    else:
        print("Student not found.")



def search_students_by_name_view():
    name = input("Enter Student Name: ")
    results = admin_controller.search_students_by_name(name)
    if results:
        for s in results:
            print(s)
    else:
        print("No matching students found.")


def filter_students_by_subject_view():
    subject = input("Enter Subject Name: ")
    students = admin_controller.filter_students_by_subject(subject)
    if students:
        for s in students:
            print(s)
    else:
        print("No students enrolled in this subject.")


def view_login_statistics():
    stats = admin_controller.fetch_login_statistics()
    if stats:
        for user_id, count in stats.items():
            print(f"User {user_id}: {count} logins")
    else:
        print("No login data available.")


